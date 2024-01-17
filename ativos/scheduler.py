# scheduler.py
from apscheduler.schedulers.background import BackgroundScheduler
# scheduler.py

from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from django.conf import settings

from ativos.tasks import monitorar_ativo_e_enviar_email

executors = {
    'default': ThreadPoolExecutor(10),
    'processpool': ProcessPoolExecutor(5)
}

job_defaults = {
    'coalesce': False,
    'max_instances': 1
}

scheduler = BackgroundScheduler(executors=executors, job_defaults=job_defaults)

def start():
    scheduler.add_job(monitorar_ativo_e_enviar_email, 'interval', minutes=2)  # Executa a cada 2 minutos
    scheduler.start()  # Inicia o scheduler após adicionar os jobs

# A função start deve ser chamada de algum lugar que seja executado quando o Django estiver pronto.
