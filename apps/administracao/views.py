
from django.contrib.auth.decorators import user_passes_test
from django.db import transaction
from django.shortcuts import render, redirect, reverse
from .models import Reserva, Usuario,  Cupons
from .models import Apartamento
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import FormMainPage, ReservaFormCreate, RelatorioReservasForm, RelatorioUsuariosForm
from django.views.generic import FormView, UpdateView, CreateView
from .forms import CreateAccountForm
from django.http import request, JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetView
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.urls import reverse_lazy
import requests
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from django.http import HttpResponse
import io




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



class HomehospedagemNovo(LoginRequiredMixin, CreateView):
    model = Reserva
    form_class = ReservaFormCreate

    def get_weather(self):
        url = "https://api.hgbrasil.com/weather?woeid=90200648"
        response = requests.get(url)
        data = response.json()
        return data

    def get_condition_icon_url(self, condition_slug):
        base_url = "https://assets.hgbrasil.com/weather/icons/conditions/"
        return base_url + condition_slug + ".svg"

    def get_moon_phase_icon_url(self, moon_phase):
        base_url = "https://assets.hgbrasil.com/weather/icons/moon/"
        return base_url + moon_phase.replace(" ", "_") + ".png"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        weather_data = self.get_weather()
        context['weather_data'] = weather_data
        context['apartamentos'] = Apartamento.objects.filter(status=True)

        condition_slug = weather_data["results"]["condition_slug"]
        moon_phase = weather_data["results"]["moon_phase"]

        condition_icon_url = self.get_condition_icon_url(condition_slug)
        moon_phase_icon_url = self.get_moon_phase_icon_url(moon_phase)

        context['condition_icon_url'] = condition_icon_url
        context['moon_phase_icon_url'] = moon_phase_icon_url

        return context
    def get_form_kwargs(self):
        kwargs = super(HomehospedagemNovo, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs
    def form_valid(self, form):
        reserva_obj = form.save(commit=False)
        reserva_obj.user = self.request.user

        if reserva_obj.dataEntrada and reserva_obj.dataSaida and reserva_obj.dataEntrada < reserva_obj.dataSaida:
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
                    with transaction.atomic():
                        cupom = Cupons.objects.select_for_update().get(codigo=codigo_cupom, utilizado=False)
                        reserva_obj.valor -= cupom.desconto
                        if reserva_obj.valor < 0:
                            reserva_obj.valor = 0  # Garantindo que o valor não seja negativo
                        cupom.utilizado = True
                        self.request.user.cupons_utilizados.add(cupom)
                        cupom.save()
                        reserva_obj.cupons = cupom
                except Cupons.DoesNotExist:
                    pass

            super().form_valid(form)
            reserva_obj.save()
            return super().form_valid(form)
        else:
            messages.add_message(self.request, constants.ERROR, 'Esse intervalo de data  está invalido')
            return redirect(reverse('administracao:create_reserva'))


class CustomPasswordResetView(PasswordResetView):
    email_template_name = 'registration/password_reset_email.html'
    success_url = reverse_lazy('password_reset_done')

    def form_valid(self, form):
        email = form.cleaned_data['email']
        associated_users = Usuario.objects.filter(email=email)

        for user in associated_users:
            new_password = Usuario.objects.make_random_password()
            user.set_password(new_password)
            user.save()


            subject = 'Password Reset Requested'
            email_template_name = 'registration/password_reset_email.html'
            c = {
                'email': user.email,
                'domain': self.request.META['HTTP_HOST'],
                'site_name': 'Pousada Praia Campeche',
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'user': user,
                'token': default_token_generator.make_token(user),
                'new_password': new_password,
            }
            email = render_to_string(email_template_name, c)
            send_mail(subject, email, 'augusto.tavares.a@gmail.com', [user.email], fail_silently=False)

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
    datas_ocupadas = apartamento.qntDias


    datas_ocupadas_reais = []
    if datas_ocupadas:
        for data_str in datas_ocupadas.split(', '):
            data = datetime.strptime(data_str, '%d-%m-%Y').date()
            datas_ocupadas_reais.append(data)


    intervalo_total = (datetime.now().date() + timedelta(days=365)) - datetime.now().date()
    datas_disponiveis = []
    if datas_ocupadas_reais:
        data_atual = datetime.now().date()
        while data_atual <= datetime.now().date() + intervalo_total:
            if data_atual not in datas_ocupadas_reais:
                datas_disponiveis.append(data_atual.strftime('%d/%m/%Y'))
            data_atual += timedelta(days=1)
    else:
        datas_disponiveis = [datetime.now().date() + timedelta(days=i) for i in range(intervalo_total.days)]
        datas_disponiveis = [data.strftime('%d/%m/%Y') for data in datas_disponiveis]

    return JsonResponse({'valor': valor, 'datas_disponiveis': datas_disponiveis})



def is_superuser(user):
    return user.is_superuser

@user_passes_test(is_superuser)
def relatorio_reservas(request):
    if request.method == 'POST':
        form = RelatorioReservasForm(request.POST)
        if form.is_valid():
            data_inicio = form.cleaned_data['data_inicio']
            data_fim = form.cleaned_data['data_fim']

            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="relatorio_reservas.pdf"'

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            data = []

            reservas = Reserva.objects.filter(user=request.user, dataEntrada__gte=data_inicio, dataSaida__lte=data_fim)

            data.append([ 'Data Entrada', 'Data Saída','Apartamento', 'Cliente', 'Valor'])
            total_valor = 0
            for reserva in reservas:
                data.append([ reserva.dataEntrada.strftime('%d-%m-%Y'),
                             reserva.dataSaida.strftime('%d-%m-%Y'),reserva.apartamento, reserva.user, f'R${reserva.valor:.2f}'])
                total_valor += reserva.valor


            data.append([ '','','', 'Total:', f'R${total_valor:.2f}'])


            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)


            doc.build([table])

            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)

            return response
    else:
        form = RelatorioReservasForm()

    return render(request, 'relatorio_template.html', {'form': form})


@user_passes_test(is_superuser)
def relatorio_usuarios(request):
    if request.method == 'POST':
        form = RelatorioUsuariosForm(request.POST)
        if form.is_valid():
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="relatorio_usuarios.pdf"'

            buffer = io.BytesIO()
            doc = SimpleDocTemplate(buffer, pagesize=letter)
            data = []

            usuarios = Usuario.objects.all()

            data.append(['Data Ultimo Login', 'Usuário', 'E-mail', 'CPF',  'Cupons Utilizados'])

            for usuario in usuarios:
                cupons_utilizados = ', '.join([cupom.codigo for cupom in usuario.cupons_utilizados.all()])
                data.append([usuario.date_joined.strftime('%d-%m-%Y'), usuario.username, usuario.email, usuario.cpf, cupons_utilizados])

            table = Table(data)
            style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                                ('GRID', (0, 0), (-1, -1), 1, colors.black)])
            table.setStyle(style)

            doc.build([table])

            pdf = buffer.getvalue()
            buffer.close()
            response.write(pdf)

            return response
    else:
        form = RelatorioUsuariosForm()

    return render(request, 'relatorio_cupons.html', {'form': form})
