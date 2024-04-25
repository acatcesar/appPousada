from django.shortcuts import render, redirect, reverse
from django.db import models
from .models import Reserva, Usuario
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import CriarContaForm, FormMainPage
from django.views.generic import TemplateView, ListView, DetailView, FormView, UpdateView


class MainPage(LoginRequiredMixin, ListView):

    model = Reserva
    paginate_by = 10

    def listing(request):
        local_list = Reserva.objects.all()

        return render(request, "homehospedagem_list.html")    


# class MainPage(FormView):
#     template_name = "mainpage.html"
#     form_class = FormMainPage

#     def get(self, request, *args, **kwargs):
#         if request.user.is_authenticated: 

#             return redirect('administracao:homehospedagem')
#         else:
#             return super().get(request, *args, **kwargs)  

#     def get_success_url(self):
#         email = self.request.POST.get("email")
#         usuarios = Usuario.objects.filter(email=email)
#         if usuarios:
#             return reverse('administracao:login')
#         else:
#             return reverse('administracao:createaccount')


class Homehospedagem(LoginRequiredMixin, ListView):
    model = Reserva