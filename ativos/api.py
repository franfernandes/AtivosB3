import requests
from decouple import config
import yfinance as yf
import logging


B3_API_KEY = config('B3_API_KEY')

def obter_ativos_b3():
    url = 'https://brapi.dev/api/available'  
    headers = {'Authorization': f'Bearer {B3_API_KEY}'}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()  
    else:
       
        response.raise_for_status()

logger = logging.getLogger(__name__)

def obter_detalhes_ativo_yahoo(ticker):
    logger.info(f"Obtendo detalhes para o ativo: {ticker}")
    try:
        ativo = yf.Ticker(ticker)
        info = ativo.info
        abertura = info.get('open', 0)
        fechamento = info.get('previousClose', 0)
        cotacao = info.get('currentPrice', 0)
        variacao_percentual = ((cotacao - abertura) / abertura) * 100 if abertura else 0

        detalhes_ativo = {
            'codigo': ticker,
            'nome': info.get('longName', 'Nome indisponível'),
            'abertura': abertura,
            'fechamento': fechamento,
            'cotacao': cotacao,
            'variacao_percentual': variacao_percentual,
        }
        logger.info(f"Detalhes obtidos para o ativo {ticker}: {detalhes_ativo}")
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            print(f"Ativo não encontrado: {ticker}")
        else:
            print(f"Erro ao acessar os dados do ativo {ticker}: {e}")
        detalhes_ativo = {
            'codigo': ticker,
            'nome': 'Nome indisponível',
            'abertura': 0,
            'fechamento': 0,
            'cotacao': 0,
            'variacao_percentual': 0,
        }
        print(f"Detalhes do ativo {ticker}: {detalhes_ativo}")

        logger.error(f"HTTP Error ao acessar os dados do ativo {ticker}: {e}")
    except Exception as e:
        print(f"Erro inesperado ao obter informações do ativo {ticker}: {e}")
        detalhes_ativo = {
            'codigo': ticker,
            'nome': 'Nome indisponível',
            'abertura': 0,
            'fechamento': 0,
            'cotacao': 0,
            'variacao_percentual': 0,
        }
        logger.error(f"Erro inesperado ao obter informações do ativo {ticker}: {e}")
    return detalhes_ativo
