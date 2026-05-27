from django.urls import path

from .views import (
    desmonitorar_ativo_view,
    editar_ativo_view,
    listar_ativos,
    meus_ativos_view,
    monitorar_ativo_form_view,
    monitorar_ativo_view,
)


urlpatterns = [
    path("listar_ativos/", listar_ativos, name="listar_ativos"),
    path("monitorar/<str:codigo>/", monitorar_ativo_view, name="monitorar_ativo_view"),
    path(
        "definir_limites/<str:codigo>/",
        monitorar_ativo_form_view,
        name="monitorar_ativo_form",
    ),
    path(
        "desmonitorar/<str:codigo>/",
        desmonitorar_ativo_view,
        name="desmonitorar_ativo_view",
    ),
    path("meus_ativos/", meus_ativos_view, name="meus_ativos"),
    path("editar_ativo/<str:codigo>/", editar_ativo_view, name="editar_ativo"),
]
