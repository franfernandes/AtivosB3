from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings

class Ativo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    fechamento = models.DecimalField(max_digits=10, decimal_places=2)
    abertura = models.DecimalField(max_digits=10, decimal_places=2)
    cotacao = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    variacao_percentual = models.DecimalField(max_digits=5, decimal_places=2)
    limiar_compra = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    limiar_venda = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    usuarios_monitorando = models.ManyToManyField(User, related_name='ativos_monitorados')
    frequencia_monitoramento = models.IntegerField(default=60)  # Em minutos
    ultimo_check = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    def deve_ser_monitorado(self):
        if self.ultimo_check is None:
            return True
        return timezone.now() >= self.ultimo_check + timezone.timedelta(minutes=self.frequencia_monitoramento)
