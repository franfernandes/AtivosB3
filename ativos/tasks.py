import logging
from django.core.mail import send_mail
from .models import Ativo
import yfinance as yf

# Configuração do Logger
logger = logging.getLogger(__name__)

def obter_cotacao_atual(ticker):
    try:
        ativo = yf.Ticker(ticker)
        info = ativo.info
        return info.get('regularMarketPrice')
    except Exception as e:
        logger.error(f"Erro ao obter cotação atual do ativo {ticker}: {e}")
        return None

def enviar_email_compra(usuario_email, ativo, cotacao_atual):
    try:
        send_mail(
            'Recomendação de Compra',
            f'O ativo {ativo.nome} está com uma cotação atrativa para compra: R${cotacao_atual}',
            'gygacliente@gmail.com',
            [usuario_email],
            fail_silently=False,
        )
        logger.info(f"Email de compra enviado para {usuario_email}")
    except Exception as e:
        logger.error(f"Erro ao enviar email de compra para {usuario_email}: {e}")

def enviar_email_venda(usuario_email, ativo, cotacao_atual):
    try:
        send_mail(
            'Recomendação de Venda',
            f'O ativo {ativo.nome} alcançou um preço de venda recomendado: R${cotacao_atual}',
            'gygacliente@gmail.com',
            [usuario_email],
            fail_silently=False,
        )
        logger.info(f"Email de venda enviado para {usuario_email}")
    except Exception as e:
        logger.error(f"Erro ao enviar email de venda para {usuario_email}: {e}")

def monitorar_ativo_e_enviar_email():
    ativos_monitorados = Ativo.objects.filter(usuarios_monitorando__isnull=False).distinct()
    for ativo in ativos_monitorados:
        cotacao_atual = ativo.cotacao
        emails_enviados = []

        if cotacao_atual is None:
            logger.error(f"Cotação atual não disponível para o ativo {ativo.codigo}")
            continue

        if ativo.limiar_compra and cotacao_atual <= ativo.limiar_compra:
            for usuario in ativo.usuarios_monitorando.all():
                email_destino = usuario.username  # Usando username como e-mail
                print(f"Preparando para enviar email de compra para {email_destino}")
                try:
                    send_mail(
                        'Recomendação de Compra',
                        f'O ativo {ativo.nome} atingiu o seu limiar de compra: R${cotacao_atual}',
                        'gygacliente@gmail.com',
                        [email_destino],
                        fail_silently=False,
                    )
                    emails_enviados.append(email_destino)
                    logger.info(f"Email de compra enviado para {email_destino} sobre o ativo {ativo.codigo}")
                except Exception as e:
                    logger.error(f"Erro ao enviar email de compra para {email_destino}: {e}")

        # Repita o processo acima para a lógica de envio de e-mails de venda...

        if emails_enviados:
            logger.info(f"Emails enviados para {', '.join(emails_enviados)} sobre o ativo {ativo.codigo}")
        else:
            logger.info(f"Nenhum email enviado para o ativo {ativo.codigo}")