
import logging
from apscheduler.schedulers.background import BackgroundScheduler


logger = logging.getLogger(__name__)


scheduler = BackgroundScheduler()

def agendar_tarefa_monitoramento(ativo, frequencia):
    
    from django_apscheduler.jobstores import DjangoJobStore
    from ativos.tasks import monitorar_ativo_e_enviar_email
    from django_apscheduler.models import DjangoJobExecution

    
    job_id = f"monitorar_ativo_{ativo.codigo}"

    try:
        
        job_existente = scheduler.get_job(job_id=job_id, jobstore="default")

        
        if job_existente:
            scheduler.remove_job(job_id=job_id, jobstore="default")
            logger.info(f"Job existente para o ativo {ativo.codigo} removido.")

        
        scheduler.add_job(
            monitorar_ativo_e_enviar_email, 
            'interval', 
            minutes=frequencia, 
            id=job_id, 
            replace_existing=True
        )
        logger.info(f"Job agendado para o ativo {ativo.codigo} com frequência de {frequencia} minutos.")

        
        if not scheduler.running:
            scheduler.start()
            logger.info("Agendador iniciado.")
    
    except Exception as e:
        logger.error(f"Erro ao agendar job para o ativo {ativo.codigo}: {e}")



