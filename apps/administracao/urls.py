from django.urls import path, reverse_lazy

from .views import MainPage, CreateAccount, Editaccount, HomehospedagemNovo, \
    obter_apartamento_valor, relatorio_reservas, relatorio_usuarios, CustomPasswordResetView
from django.contrib.auth import views as auth_view
from django.urls import path

app_name ='administracao'

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('novo/', HomehospedagemNovo.as_view(), name='create_reserva'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('createaccount/', CreateAccount.as_view(), name='createaccount'),
    path('editaccount/<int:pk>/', Editaccount.as_view(), name='editaccount'),
    path('obter_apartamento_valor/', obter_apartamento_valor, name='obter_apartamento_valor'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name='editarperfil.html', success_url=reverse_lazy('administracao:novo')),
         name='mudarsenha'),
    path('relatorio_reservas/', relatorio_reservas, name='relatorio_reservas'),
    path('relatorio_usuarios/', relatorio_usuarios, name='relatorio_usuarios'),
    path('reset_password/', CustomPasswordResetView.as_view(), name='reset_password'),

]

