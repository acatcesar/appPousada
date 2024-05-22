from django.contrib.auth.forms import UserCreationForm
from .models import Usuario, Apartamento, Reserva
from django import forms
from django.forms import ModelForm

class FormMainPage(forms.Form):
    email = forms.EmailField(label=False)


class CreateAccountForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = Usuario
        fields = ('username', 'email', 'password1', 'password2')


class ReservaFormCreate(ModelForm):

    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apartamento'].queryset = Apartamento.objects.all()

    class Meta:
        model = Reserva
        fields = ['apartamento','valor','dataEntrada','dataSaida','qntDias','cupons']

