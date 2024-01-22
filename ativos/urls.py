from django.urls import path
from ativos import views
from .views import (
    listar_ativos,
    acompanhamento_ativo,
    signup,
    monitorar_ativo_view,
    monitorar_ativo_form_view,
    desmonitorar_ativo_view
)
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.home_view, name='home'),  # Esta é a URL para a view da página inicial
    
    path('signup/', signup, name='signup'),  
    path('listar_ativos/', listar_ativos, name='listar_ativos'),
    path('acompanhamento/<int:pk>/', acompanhamento_ativo, name='acompanhamento_ativo'),
    path('monitorar/<str:codigo>/', monitorar_ativo_view, name='monitorar_ativo_view'),
    path('definir_limites/<str:codigo>/', monitorar_ativo_form_view, name='monitorar_ativo_form'),
    path('desmonitorar/<str:codigo>/', desmonitorar_ativo_view, name='desmonitorar_ativo_view'),
    path('meus_ativos/', views.meus_ativos_view, name='meus_ativos'),
    path('editar_ativo/<str:codigo>/', views.editar_ativo_view, name='editar_ativo'),
    


]
