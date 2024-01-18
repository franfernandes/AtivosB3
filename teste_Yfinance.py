import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investidor.settings')
django.setup()

from ativos.api import obter_detalhes_ativo_yahoo

if __name__ == '__main__':
    ticker = 'MGLU3.SA' 
    detalhes = obter_detalhes_ativo_yahoo(ticker)
    print(detalhes)
