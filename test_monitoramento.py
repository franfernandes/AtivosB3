import os
import django

# Configure as settings do Django para o script poder funcionar fora do contexto de uma aplicação web.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investidor.settings')
django.setup()

# Agora você pode importar suas views e modelos, pois o Django já foi configurado.
from ativos.tasks import monitorar_ativo_e_enviar_email

if __name__ == '__main__':
    # Chama a função sem argumentos, pois agora ela é responsável por verificar todos os ativos.
    monitorar_ativo_e_enviar_email()
