# investidor/celery.py
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'investidor.settings')

app = Celery('investidor')

# Usando o banco de dados para armazenar os resultados das tarefas
app.config_from_object('django.conf:settings', namespace='CELERY')

# Carregar módulos de tarefa de todas as aplicações registradas no Django
app.autodiscover_tasks()
