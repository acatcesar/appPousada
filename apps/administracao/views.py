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

    def form_valid(self, form):
        reserva_obj = form.save(commit=False)
        reserva_obj.user = self.request.user

        if reserva_obj.dataEntrada and reserva_obj.dataSaida:
            datas_entre = []
            current_date = reserva_obj.dataEntrada
            while current_date <= reserva_obj.dataSaida:
                datas_entre.append(current_date.date())
                current_date += timezone.timedelta(days=1)
            reserva_obj.qntDatas = len(datas_entre)
            reserva_obj.qntDias = ', '.join([str(date) for date in datas_entre])
        reserva_obj.valor *= reserva_obj.qntDatas


        codigo_cupom = self.request.POST.get('codigo_cupom')
        if codigo_cupom:
            try:
                cupom = Cupons.objects.get(codigo=codigo_cupom, utilizado=False)
                reserva_obj.valor -= cupom.desconto
                cupom.utilizado = True
                cupom.save()
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
    fields = ['first_name', 'last_name', 'email']

    # def get_success_url(self):
    #     return reverse('administracao:reserva')


def obter_apartamento_valor(request):
    apartamento_id = request.GET.get('apartamento_id')
    apartamento = Apartamento.objects.get(id=apartamento_id)
    valor = apartamento.valor

    return JsonResponse({'valor': valor})


class Apartamentolista(ListView):
    model = Apartamento
