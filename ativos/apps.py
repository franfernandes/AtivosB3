

import logging
from django.apps import AppConfig
from ativos.scheduler import scheduler  

logger = logging.getLogger(__name__)  

class AtivosConfig(AppConfig):
    name = 'ativos'

    def ready(self):
        
        if not scheduler.running:
            scheduler.start()
            logger.info("Agendador iniciado na configuração do aplicativo.")
