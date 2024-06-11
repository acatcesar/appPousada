from django.urls import path, reverse_lazy

from . import views
from .views import MainPage, Homehospedagem, CreateAccount, Editaccount, HomehospedagemNovo, \
    obter_apartamento_valor, Apartamentolista, relatorio_reservas
from django.contrib.auth import views as auth_view
from django.urls import path

app_name ='administracao'

urlpatterns = [
    path('', MainPage.as_view(), name='home'),
    path('reserva/', Homehospedagem.as_view(), name='reserva'),
    path('novo/', HomehospedagemNovo.as_view(), name='create_reserva'),
    path('login/', auth_view.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('createaccount/', CreateAccount.as_view(), name='createaccount'),

    path('editaccount/<int:pk>/', Editaccount.as_view(), name='editaccount'),

    path('homehospedagem', Homehospedagem.as_view(), name='homehospedagem'),
    path('obter_apartamento_valor/', obter_apartamento_valor, name='obter_apartamento_valor'),
    path('apartamento/', Apartamentolista.as_view(), name='apartamento'),
    path('mudarsenha/', auth_view.PasswordChangeView.as_view(template_name='editarperfil.html', success_url=reverse_lazy('administracao:novo')),
         name='mudarsenha'),
    path('gerar_relatorio/', relatorio_reservas, name='gerar_relatorio'),

    # path('gerar_relatorio/<start_date>/<end_date>/', relatorio_reservas, name='gerar_relatorio'),

]

