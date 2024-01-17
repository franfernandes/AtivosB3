import os
import django

# Defina a variável de ambiente para o seu arquivo de configurações do Django.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investidor.settings')

# Carregue as configurações do Django.
django.setup()

# Agora você pode importar suas tarefas e modelos do Django.
from ativos.tasks import tarefa_de_exemplo

# Execute a tarefa diretamente.
resultado = tarefa_de_exemplo()
print(resultado)
