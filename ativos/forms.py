from django import forms
from .models import Ativo

class AtivoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['codigo', 'nome', ]


class AtivoMonitoramentoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = ['limiar_compra', 'limiar_venda', 'frequencia_monitoramento',]
