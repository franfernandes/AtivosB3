# apps.py dentro do aplicativo 'ativos'

from django.apps import AppConfig

class AtivosConfig(AppConfig):
    name = 'ativos'

    def ready(self):
        from ativos.scheduler import start
        start()
