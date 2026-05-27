import logging
from decimal import Decimal

from django.conf import settings
from django.core.mail import send_mail
from django.utils import timezone

from .api import obter_detalhes_ativo
from .models import Ativo


logger = logging.getLogger(__name__)


def obter_cotacao_atual(ticker: str) -> Decimal | None:
    """Busca a cotacao mais recente do ativo."""
    valor = obter_detalhes_ativo(ticker).get("cotacao")
    return Decimal(str(valor)) if valor else None


def enviar_email_compra(usuario_email: str, ativo: Ativo, cotacao_atual: Decimal) -> None:
    """Notifica um usuario quando o ativo atinge o limite de compra."""
    send_mail(
        "Recomendacao de Compra",
        f"O ativo {ativo.nome} esta com uma cotacao atrativa para compra: R${cotacao_atual}",
        settings.DEFAULT_FROM_EMAIL,
        [usuario_email],
        fail_silently=False,
    )


def enviar_email_venda(usuario_email: str, ativo: Ativo, cotacao_atual: Decimal) -> None:
    """Notifica um usuario quando o ativo atinge o limite de venda."""
    send_mail(
        "Recomendacao de Venda",
        f"O ativo {ativo.nome} alcancou um preco de venda recomendado: R${cotacao_atual}",
        settings.DEFAULT_FROM_EMAIL,
        [usuario_email],
        fail_silently=False,
    )


def monitorar_ativo_e_enviar_email(ativo_id: int | None = None) -> None:
    """Atualiza cotacoes monitoradas e envia alertas conforme os limites."""
    ativos_monitorados = Ativo.objects.filter(
        usuarios_monitorando__isnull=False
    ).distinct()
    if ativo_id is not None:
        ativos_monitorados = ativos_monitorados.filter(pk=ativo_id)

    for ativo in ativos_monitorados:
        cotacao_atual = obter_cotacao_atual(ativo.codigo)
        if cotacao_atual is None:
            logger.warning("Cotacao atual indisponivel para o ativo %s", ativo.codigo)
            continue

        ativo.cotacao = cotacao_atual
        ativo.ultimo_check = timezone.now()
        ativo.save(update_fields=["cotacao", "ultimo_check"])

        for usuario in ativo.usuarios_monitorando.all():
            destinatario = usuario.email or usuario.username
            if ativo.limiar_compra and cotacao_atual <= ativo.limiar_compra:
                enviar_email_compra(destinatario, ativo, cotacao_atual)
            if ativo.limiar_venda and cotacao_atual >= ativo.limiar_venda:
                enviar_email_venda(destinatario, ativo, cotacao_atual)
