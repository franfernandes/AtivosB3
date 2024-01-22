from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


class Ativo(models.Model):
    codigo = models.CharField(max_length=10, unique=True)
    nome = models.CharField(max_length=100)
    fechamento = models.DecimalField(max_digits=10, decimal_places=2)
    abertura = models.DecimalField(max_digits=10, decimal_places=2)
    cotacao = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    variacao_percentual = models.DecimalField(max_digits=5, decimal_places=2)
    limiar_compra = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    limiar_venda = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    usuarios_monitorando = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name="ativos_monitorados"
    )
    frequencia_monitoramento = models.IntegerField(default=2)
    ultimo_check = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.codigo} - {self.nome}"

    def deve_ser_monitorado(self):
        if self.ultimo_check is None:
            return True
        return timezone.now() >= self.ultimo_check + timezone.timedelta(
            minutes=self.frequencia_monitoramento
        )


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, blank=True)

    class Meta:
        db_table = "custom_user"

    groups = models.ManyToManyField(
        "auth.Group",
        verbose_name=_("groups"),
        blank=True,
        help_text=_(
            "The groups this user belongs to. A user will get all permissions "
            "granted to each of their groups."
        ),
        related_name="custom_user_set",
        related_query_name="user",
    )
    user_permissions = models.ManyToManyField(
        "auth.Permission",
        verbose_name=_("user permissions"),
        blank=True,
        help_text=_("Specific permissions for this user."),
        related_name="custom_user_permission_set",
        related_query_name="user",
    )
