from django import forms
from .models import Ativo
from django.contrib.auth.forms import AuthenticationForm

class AtivoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['codigo', 'nome', ]


class AtivoMonitoramentoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['limiar_compra', 'limiar_venda', 'frequencia_monitoramento',]




class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")
