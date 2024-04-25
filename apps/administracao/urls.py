from django.urls import path, reverse_lazy
from .views import MainPage, Homehospedagem
from django.contrib.auth import views as auth_view
from django.urls import path



urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('reserva/', Homehospedagem.as_view(), name='reserva'),
]