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
        fields = ('username', 'email', 'password1', 'password2', 'cpf', 'endereco', 'celular')

class ReservaFormCreate(ModelForm):

    dataEntrada = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))
    dataSaida = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'))


    def __init__(self, user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['apartamento'].queryset = Apartamento.objects.all()

    class Meta:
        model = Reserva
        fields = ['apartamento','dataEntrada','dataSaida', 'cupons', 'valor']

class RelatorioReservasForm(forms.Form):
    data_inicio = forms.DateField(label='Data de Início')
    data_fim = forms.DateField(label='Data de Fim')

class RelatorioUsuariosForm(forms.Form):
    pass