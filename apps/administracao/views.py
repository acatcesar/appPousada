from django.shortcuts import render, redirect, reverse
from django.db import models
from .models import Reserva, Usuario
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import  FormMainPage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView
from .forms import CreateAccountForm

# class MainPage(LoginRequiredMixin, ListView):

#     model = Reserva
#     paginate_by = 10

#     def listing(request):
#         local_list = Reserva.objects.all()

#         return render(request, "homehospedagem_list.html")    


class MainPage(FormView):
    template_name = "mainpage.html"
    form_class = FormMainPage

    # def get(self, request, *args, **kwargs):
    #     if request.user.is_authenticated: 

            # return redirect('administracao:homehospedagem')
    #     else:
    #         return super().get(request, *args, **kwargs)  

    # def get_success_url(self):
    #     email = self.request.POST.get("email")
    #     usuarios = Usuario.objects.filter(email=email)
    #     if usuarios:
    #         return reverse('administracao:login')
    #     else:
    #         return reverse('administracao:createaccount')


class Homehospedagem(LoginRequiredMixin, ListView):
    model = Reserva


class CreateAccount(FormView):
    template_name = "createaccount.html"
    form_class = CreateAccountForm

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)