from django import forms
from .models import Ativo
from django.contrib.auth.forms import AuthenticationForm
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class AtivoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = [
            "codigo",
            "nome",
        ]


class AtivoMonitoramentoForm(forms.ModelForm):
    class Meta:
        model = Ativo
        fields = [
            "limiar_compra",
            "limiar_venda",
            "frequencia_monitoramento",
        ]


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")


from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=30, help_text="Required.")
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
