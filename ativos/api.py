import logging

import requests
import truststore
from decouple import config


logger = logging.getLogger(__name__)
DEMO_TICKERS = ["PETR4", "MGLU3", "VALE3", "ITUB4"]

# Reuse the operating system certificate store for external HTTPS integrations.
truststore.inject_into_ssl()


def _headers() -> dict[str, str]:
    api_key = config("BRAPI_API_KEY", default="")
    return {"Authorization": f"Bearer {api_key}"} if api_key else {}


def obter_ativos_b3() -> dict:
    """Retorna tickers disponíveis, ou a carteira de demonstração sem token."""
    if not config("BRAPI_API_KEY", default=""):
        return {"stocks": DEMO_TICKERS}

    response = requests.get(
        "https://brapi.dev/api/quote/list",
        headers=_headers(),
        params={"limit": 100, "type": "stock"},
        timeout=10,
    )
    response.raise_for_status()
    stocks = [item["stock"] for item in response.json().get("stocks", [])]
    return {"stocks": stocks}


def obter_detalhes_ativo(ticker: str) -> dict:
    """Consulta a cotação de um ativo pela API brapi."""
    logger.info("Obtendo detalhes para o ativo: %s", ticker)
    try:
        response = requests.get(
            f"https://brapi.dev/api/quote/{ticker}",
            headers=_headers(),
            timeout=10,
        )
        response.raise_for_status()
        info = response.json()["results"][0]
        return {
            "codigo": info["symbol"],
            "nome": info.get("longName", "Nome indisponível"),
            "abertura": info.get("regularMarketOpen", 0),
            "fechamento": info.get("regularMarketPreviousClose", 0),
            "cotacao": info.get("regularMarketPrice", 0),
            "variacao_percentual": info.get("regularMarketChangePercent", 0),
        }
    except (KeyError, IndexError, requests.RequestException) as exc:
        logger.error("Erro ao obter informações do ativo %s: %s", ticker, exc)
        return {
            "codigo": ticker,
            "nome": "Nome indisponível",
            "abertura": 0,
            "fechamento": 0,
            "cotacao": 0,
            "variacao_percentual": 0,
        }
