from django.shortcuts import render, redirect, reverse
from django.db import models
from .models import Reserva, Usuario, Apartamento
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  FormMainPage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView, CreateView
from .forms import CreateAccountForm

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
    fields = ['dataEntrada', 'dataSaida', 'qntDias', 'apartamento', 'cupons']  # Substitua pelos nomes dos campos que deseja incluir no formulário



    # def get_form_kwargs(self):
    #     kwargs = super(HomehospedagemNovo, self).get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

    # def get_form_kwargs(self):
    #     kwargs = super(Homehospedagem, self).get_form_kwargs()
    #     kwargs.update({'user': self.request.user})
    #     return kwargs

    # def form_valid (self, form):
    #     apropriacao_obj = form.save (commit=False)
    #
    #     return self.form_invalid(form)



class Apartamento(ListView):
    model = Apartamento


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