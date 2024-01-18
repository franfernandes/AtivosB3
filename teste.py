import os
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investidor.settings')


django.setup()


from ativos.tasks import tarefa_de_exemplo


resultado = tarefa_de_exemplo()
print(resultado)
