from decimal import Decimal
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse

from .api import DEMO_TICKERS, obter_ativos_b3, obter_detalhes_ativo
from .models import Ativo, CustomUser
from .tasks import monitorar_ativo_e_enviar_email


class BrapiClientTests(TestCase):
    @patch("ativos.api.config", return_value="")
    def test_sem_token_utiliza_tickers_liberados_para_demonstracao(
        self, mock_config
    ) -> None:
        self.assertEqual(obter_ativos_b3(), {"stocks": DEMO_TICKERS})

    @patch("ativos.api.config", return_value="")
    @patch("ativos.api.requests.get")
    def test_converte_resposta_de_cotacao_para_modelo_da_aplicacao(
        self, mock_get, mock_config
    ) -> None:
        response = mock_get.return_value
        response.json.return_value = {
            "results": [
                {
                    "symbol": "PETR4",
                    "longName": "Petrobras",
                    "regularMarketOpen": 42.10,
                    "regularMarketPreviousClose": 42.00,
                    "regularMarketPrice": 43.44,
                    "regularMarketChangePercent": 3.43,
                }
            ]
        }

        detalhe = obter_detalhes_ativo("PETR4")

        self.assertEqual(detalhe["codigo"], "PETR4")
        self.assertEqual(detalhe["cotacao"], 43.44)
        mock_get.assert_called_once()


class ListarAtivosViewTests(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username="fran@example.com",
            email="fran@example.com",
            password="senha-forte-123",
        )
        self.client.force_login(self.user)

    def test_home_autenticada_mantem_acesso_a_listagem(self) -> None:
        response = self.client.get(reverse("home"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Listar Ativos")

    @patch("ativos.views.obter_detalhes_ativo")
    @patch("ativos.views.obter_ativos_b3")
    def test_lista_persiste_fechamento_recebido_da_api(
        self, mock_ativos_b3, mock_detalhes
    ) -> None:
        mock_ativos_b3.return_value = {"stocks": ["PETR4"]}
        mock_detalhes.return_value = {
            "codigo": "PETR4",
            "nome": "Petrobras",
            "fechamento": Decimal("31.25"),
            "abertura": Decimal("31.00"),
            "cotacao": Decimal("31.80"),
            "variacao_percentual": Decimal("2.58"),
        }

        response = self.client.get(reverse("listar_ativos"))

        self.assertEqual(response.status_code, 200)
        ativo = Ativo.objects.get(codigo="PETR4")
        self.assertEqual(ativo.fechamento, Decimal("31.25"))

    @patch("ativos.views.obter_detalhes_ativo")
    @patch("ativos.views.obter_ativos_b3")
    def test_lista_consulta_apenas_ativos_da_pagina_atual(
        self, mock_ativos_b3, mock_detalhes
    ) -> None:
        mock_ativos_b3.return_value = {
            "stocks": [f"ATIVO{i}" for i in range(15)]
        }
        mock_detalhes.side_effect = lambda ticker: {
            "codigo": ticker,
            "nome": ticker,
            "fechamento": Decimal("10.00"),
            "abertura": Decimal("10.00"),
            "cotacao": Decimal("10.00"),
            "variacao_percentual": Decimal("0.00"),
        }

        response = self.client.get(reverse("listar_ativos") + "?page=2")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(mock_detalhes.call_count, 5)

    @patch("ativos.views.obter_ativos_b3", side_effect=RuntimeError("api offline"))
    def test_lista_exibe_pagina_vazia_quando_servico_externo_falha(
        self, mock_ativos_b3
    ) -> None:
        response = self.client.get(reverse("listar_ativos"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Não há ativos listados.")
        self.assertContains(response, "Não foi possível consultar as cotações agora.")

    def test_desmonitorar_exige_post(self) -> None:
        ativo = Ativo.objects.create(
            codigo="VALE3",
            nome="Vale",
            fechamento=Decimal("60.00"),
            abertura=Decimal("60.00"),
            cotacao=Decimal("60.00"),
            variacao_percentual=Decimal("0.00"),
        )
        ativo.usuarios_monitorando.add(self.user)

        response = self.client.get(reverse("desmonitorar_ativo_view", args=[ativo.codigo]))

        self.assertEqual(response.status_code, 405)
        self.assertTrue(ativo.usuarios_monitorando.filter(pk=self.user.pk).exists())

    def test_desmonitorar_remove_ativo_por_post(self) -> None:
        ativo = Ativo.objects.create(
            codigo="ITUB4",
            nome="Itau",
            fechamento=Decimal("30.00"),
            abertura=Decimal("30.00"),
            cotacao=Decimal("30.00"),
            variacao_percentual=Decimal("0.00"),
        )
        ativo.usuarios_monitorando.add(self.user)

        response = self.client.post(
            reverse("desmonitorar_ativo_view", args=[ativo.codigo])
        )

        self.assertEqual(response.status_code, 302)
        self.assertFalse(ativo.usuarios_monitorando.filter(pk=self.user.pk).exists())


class MonitoramentoTests(TestCase):
    @patch("ativos.tasks.send_mail")
    @patch("ativos.tasks.obter_cotacao_atual", return_value=Decimal("9.50"))
    def test_atualiza_cotacao_e_envia_alerta_de_compra(
        self, mock_cotacao, mock_send_mail
    ) -> None:
        user = CustomUser.objects.create_user(
            username="investidor@example.com",
            email="investidor@example.com",
            password="senha-forte-123",
        )
        ativo = Ativo.objects.create(
            codigo="MGLU3",
            nome="Magazine Luiza",
            fechamento=Decimal("11.00"),
            abertura=Decimal("10.00"),
            cotacao=Decimal("10.50"),
            variacao_percentual=Decimal("5.00"),
            limiar_compra=Decimal("10.00"),
        )
        ativo.usuarios_monitorando.add(user)

        monitorar_ativo_e_enviar_email(ativo.pk)

        ativo.refresh_from_db()
        self.assertEqual(ativo.cotacao, Decimal("9.50"))
        self.assertIsNotNone(ativo.ultimo_check)
        mock_cotacao.assert_called_once_with("MGLU3")
        mock_send_mail.assert_called_once()


class MonitoramentoFormTests(TestCase):
    def setUp(self) -> None:
        self.user = CustomUser.objects.create_user(
            username="limites@example.com",
            password="SenhaSegura!2026#Apresentacao",
        )
        self.ativo = Ativo.objects.create(
            codigo="PETR4",
            nome="Petrobras",
            fechamento=Decimal("43.00"),
            abertura=Decimal("43.00"),
            cotacao=Decimal("43.00"),
            variacao_percentual=Decimal("0.00"),
        )
        self.client.force_login(self.user)

    def test_rejeita_compra_acima_do_limite_de_venda(self) -> None:
        response = self.client.post(
            reverse("monitorar_ativo_form", args=[self.ativo.codigo]),
            {
                "limiar_compra": "50.00",
                "limiar_venda": "40.00",
                "frequencia_monitoramento": "2",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response, "O limiar de compra deve ser menor que o limiar de venda."
        )
        self.assertFalse(self.ativo.usuarios_monitorando.exists())


class RotasPublicasTests(TestCase):
    def test_cadastro_possui_url_direta(self) -> None:
        response = self.client.get(reverse("signup"))

        self.assertEqual(response.status_code, 200)
        self.assertEqual(reverse("signup"), "/signup/")

    @patch("ativos.views.obter_ativos_b3", return_value={"stocks": []})
    def test_cadastro_autentica_e_redireciona_para_listagem(
        self, mock_ativos_b3
    ) -> None:
        response = self.client.post(
            reverse("signup"),
            {
                "email": "nova@example.com",
                "first_name": "Nova",
                "password1": "SenhaSegura!2026#Apresentacao",
                "password2": "SenhaSegura!2026#Apresentacao",
            },
            follow=True,
        )

        self.assertRedirects(response, reverse("listar_ativos"))
        self.assertContains(response, "Cotação de Ativos da B3")
        self.assertTrue(CustomUser.objects.filter(email="nova@example.com").exists())

    def test_cadastro_informa_quando_email_ja_esta_em_uso(self) -> None:
        CustomUser.objects.create_user(
            username="repetido@example.com",
            email="repetido@example.com",
            password="SenhaSegura!2026#Apresentacao",
        )

        response = self.client.post(
            reverse("signup"),
            {
                "email": "repetido@example.com",
                "first_name": "Outra",
                "password1": "SenhaSegura!2026#Apresentacao",
                "password2": "SenhaSegura!2026#Apresentacao",
            },
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Já existe uma conta cadastrada com este e-mail.")
