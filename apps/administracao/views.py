import io

from django.shortcuts import render, redirect, reverse
from django.db import models
from .models import Reserva, Usuario,  Cupons
from .models import Apartamento
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FormMainPage, ReservaFormCreate
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, CreateView
from .forms import CreateAccountForm
from django.http import request, JsonResponse
from django.core.exceptions import ObjectDoesNotExist
from django.utils import timezone
from datetime import datetime, timedelta
from django.core.exceptions import ValidationError
from django.http import HttpResponseBadRequest
from django.contrib import messages
from django.contrib.messages import constants
from sqlalchemy.sql.functions import user
from reportlab.pdfgen import canvas
from django.http import HttpResponse
from django.template.loader import get_template
import xhtml2pdf.pisa as pisa

# class MainPage(LoginRequiredMixin, ListView):

#     model = Reserva
#     paginate_by = 10

#     def listing(request):
#         local_list = Reserva.objects.all()

#         return render(request, "homehospedagem_form.html")



class MainPage(FormView):
    template_name = "mainpage.html"
    form_class = FormMainPage

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:

            return redirect('administracao:create_reserva')
        else:
            return super().get(request, *args, **kwargs)

    def get_success_url(self):
        email = self.request.POST.get("email")
        usuarios = Usuario.objects.filter(email=email)
        if usuarios:
            return reverse('administracao:login')
        else:
            return reverse('administracao:createaccount')



class Homehospedagem(LoginRequiredMixin, ListView):
    model = Reserva

    # def get_form_kwargs(self):
    #     kwargs = super(Homehospedagem, self).get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

    # def form_valid (self, form):
    #     apropriacao_obj = form.save (commit=False)
    #
    #     return self.form_invalid(form)


class HomehospedagemNovo(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaFormCreate

    def get_form_kwargs(self):
        kwargs = super(HomehospedagemNovo, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['apartamentos'] = Apartamento.objects.filter(status=True)
        return context

    def form_valid(self, form):
        reserva_obj = form.save(commit=False)
        reserva_obj.user = self.request.user

        if reserva_obj.dataEntrada and reserva_obj.dataSaida:
            datas_entre = []
            current_date = reserva_obj.dataEntrada
            while current_date <= reserva_obj.dataSaida:
                datas_entre.append(current_date.strftime("%d-%m-%Y"))
                current_date += timezone.timedelta(days=1)

            reserva_obj.qntDatas = len(datas_entre)
            reserva_obj.qntDias = ', '.join([str(date) for date in datas_entre])


            apartamento_selecionado = reserva_obj.apartamento
            if apartamento_selecionado.qntDias and any(date in apartamento_selecionado.qntDias for date in datas_entre):
                messages.add_message(self.request,constants.ERROR, 'Esse intervalo de data não está disponível')
                return redirect(reverse('administracao:create_reserva'))

        reserva_obj.valor *= reserva_obj.qntDatas

        codigo_cupom = self.request.POST.get('codigo_cupom')
        if codigo_cupom:
            try:
                cupom = Cupons.objects.get(codigo=codigo_cupom, utilizado=False)
                reserva_obj.valor -= cupom.desconto
                cupom.utilizado = True
                cupom.save()
                reserva_obj.cupons = cupom
            except Cupons.DoesNotExist:
                pass

        super().form_valid(form)
        reserva_obj.save()
        return super().form_valid(form)


class CreateAccount(FormView):
    template_name = "createaccount.html"
    form_class = CreateAccountForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    def get_success_url(self):
        return reverse('administracao:login')

class Editaccount(LoginRequiredMixin, UpdateView):
    template_name = "editaccount.html"
    model = Usuario
    fields = ['first_name', 'last_name', 'email', 'cpf' ,'celular', 'endereco']

    def get_success_url(self):
        return reverse('administracao:create_reserva')


def obter_apartamento_valor(request):
    apartamento_id = request.GET.get('apartamento_id')
    apartamento = Apartamento.objects.get(id=apartamento_id)
    valor = apartamento.valor
    datas_ocupadas = apartamento.qntDias  # Obtém as datas ocupadas do apartamento

    # Converte as datas ocupadas de strings para objetos datetime
    datas_ocupadas_reais = []
    if datas_ocupadas:
        for data_str in datas_ocupadas.split(', '):
            data = datetime.strptime(data_str, '%d-%m-%Y').date()
            datas_ocupadas_reais.append(data)

    # Calcula as datas disponíveis subtraindo as datas ocupadas do intervalo total
    intervalo_total = (datetime.now().date() + timedelta(days=365)) - datetime.now().date()  # Intervalo de um ano
    datas_disponiveis = []
    if datas_ocupadas_reais:
        data_atual = datetime.now().date()
        while data_atual <= datetime.now().date() + intervalo_total:
            if data_atual not in datas_ocupadas_reais:
                datas_disponiveis.append(data_atual.strftime('%d/%m/%Y'))  # Formata a data para dia/mês/ano
            data_atual += timedelta(days=1)
    else:
        datas_disponiveis = [datetime.now().date() + timedelta(days=i) for i in range(intervalo_total.days)]
        datas_disponiveis = [data.strftime('%d/%m/%Y') for data in datas_disponiveis]  # Formata as datas

    return JsonResponse({'valor': valor, 'datas_disponiveis': datas_disponiveis})

class Apartamentolista(ListView):
    model = Apartamento

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
import io
def relatorio_reservas(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="relatorio_reservas.pdf"'

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    data = []

    reservas = Reserva.objects.filter(user=request.user)

    data.append(['Valor', 'Data Entrada', 'Data Saída'])
    for reserva in reservas:
        data.append([f'R${reserva.valor:.2f}', reserva.dataEntrada.strftime('%d-%m-%Y'), reserva.dataSaida.strftime('%d-%m-%Y')])

    # Criando uma tabela e definindo estilo
    table = Table(data)
    style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                        ('GRID', (0, 0), (-1, -1), 1, colors.black)])
    table.setStyle(style)

    # Adicionando a tabela ao documento
    doc.build([table])

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)

    return response


