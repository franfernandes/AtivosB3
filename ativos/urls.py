from django.urls import path
from .views import listar_ativos, acompanhamento_ativo, signup
from django.contrib.auth import views as auth_views
from ativos import views

urlpatterns = [
    path('signup/', signup, name='signup'),  
    path('listar_ativos/', listar_ativos, name='listar_ativos'),
    path('acompanhamento/<int:pk>/', acompanhamento_ativo, name='acompanhamento_ativo'),
    path('monitorar/<str:codigo>/', views.monitorar_ativo_view, name='monitorar_ativo_view'),
    path('definir_limites/<str:codigo>/', views.monitorar_ativo_form_view, name='monitorar_ativo_form'),

]
    
