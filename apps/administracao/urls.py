from django.urls import path, reverse_lazy
from .views import MainPage, Homehospedagem, CreateAccount
from django.contrib.auth import views as auth_view
from django.urls import path

app_name ='administracao'

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('reserva/', Homehospedagem.as_view(), name='reserva'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('createaccount/', CreateAccount.as_view(), name='createaccount'),
]