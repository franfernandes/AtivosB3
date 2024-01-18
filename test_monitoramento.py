import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investidor.settings')
django.setup()


from ativos.tasks import monitorar_ativo_e_enviar_email

if __name__ == '__main__':
    
    monitorar_ativo_e_enviar_email()
