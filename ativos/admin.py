from django.contrib import admin
from .models import Ativo


class AtivoAdmin(admin.ModelAdmin):
    list_display = [
        "codigo",
        "nome",
        "fechamento",
        "abertura",
        "cotacao",
        "variacao_percentual",
        "limiar_compra",
        "limiar_venda",
    ]
    search_fields = ["codigo", "nome"]
    list_filter = ["usuarios_monitorando"]
    filter_horizontal = ["usuarios_monitorando"]


admin.site.register(Ativo, AtivoAdmin)
