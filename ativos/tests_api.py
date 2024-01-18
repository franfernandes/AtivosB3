from api import obter_ativos_b3, obter_detalhes_ativo_yahoo

def teste_obter_ativos_b3():
    print("Testando obter_ativos_b3...")
    dados = obter_ativos_b3()
    print(dados)

def teste_obter_detalhes_ativo_yahoo():
    ticker = "MGLU3"  
    print(f"Testando obter_detalhes_ativo_yahoo para {ticker}...")
    detalhes = obter_detalhes_ativo_yahoo(ticker)
    print("Detalhes do Ativo:")
    print(f"Código: {detalhes.get('codigo')}")
    print(f"Nome: {detalhes.get('nome')}")
    print(f"Abertura: {detalhes.get('abertura')}")
    print(f"Fechamento: {detalhes.get('fechamento')}")
    print(f"Cotação: {detalhes.get('cotacao')}")
    print(f"Variação: {detalhes.get('variacao_percentual')}")

if __name__ == "__main__":
    teste_obter_ativos_b3()
    teste_obter_detalhes_ativo_yahoo()
