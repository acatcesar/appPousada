from datetime import timedelta

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
        # Aqui você filtra as datas disponíveis
        self.fields['dataEntrada'].queryset = self.get_available_dates()
        self.fields['dataSaida'].queryset = self.get_available_dates()

    def get_available_dates(self):
        reservas = Reserva.objects.all()
        datas_ocupadas = set()
        for reserva in reservas:
            # Adiciona todas as datas entre data de entrada e data de saída
            datas_ocupadas.update(set([reserva.dataEntrada + timedelta(days=i) for i in
                                       range((reserva.dataSaida - reserva.dataEntrada).days)]))
        todas_as_datas = set([data for data in datas_ocupadas])
        return todas_as_datas


    class Meta:
        model = Reserva
        fields = ['apartamento','dataEntrada','dataSaida', 'cupons', 'valor']