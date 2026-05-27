from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from .models import Ativo, CustomUser


class AtivoMonitoramentoForm(forms.ModelForm):
    limiar_compra = forms.DecimalField(
        label="Limiar compra", min_value=0, required=False
    )
    limiar_venda = forms.DecimalField(
        label="Limiar venda", min_value=0, required=False
    )
    frequencia_monitoramento = forms.IntegerField(
        label="Frequência de monitoramento (em minutos)", min_value=1
    )

    class Meta:
        model = Ativo
        fields = [
            "limiar_compra",
            "limiar_venda",
            "frequencia_monitoramento",
        ]

    def clean(self):
        cleaned_data = super().clean()
        compra = cleaned_data.get("limiar_compra")
        venda = cleaned_data.get("limiar_venda")
        if compra is not None and venda is not None and compra >= venda:
            raise forms.ValidationError(
                "O limiar de compra deve ser menor que o limiar de venda."
            )
        return cleaned_data


class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(label="Email")
    password = forms.CharField(widget=forms.PasswordInput, label="Senha")


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(label="Nome", max_length=30)
    email = forms.EmailField(required=True, label="Email")
    password1 = forms.CharField(label="Senha", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Confirme a Senha", widget=forms.PasswordInput)

    class Meta:
        model = CustomUser
        fields = ("email", "first_name", "password1", "password2")

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if CustomUser.objects.filter(username__iexact=email).exists():
            raise forms.ValidationError("Já existe uma conta cadastrada com este e-mail.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data["email"]
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user
