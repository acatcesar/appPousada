from django.utils import timezone

from django.test import TestCase
from apps.administracao.models import Reserva, Usuario

class ModelTestCase(TestCase):
    def setUp(self):
        # Criar um usuário de exemplo
        self.usuario = Usuario.objects.create(
            username='testeusuario',
            first_name='Teste',
            last_name='Usuário',
            email='teste@exemplo.com',
            cpf='12345678900',
            celular='(99) 99999-9999',
            endereco='Rua Exemplo, 123'
        )

        # Criar uma reserva de exemplo associada ao usuário
        self.reserva = Reserva.objects.create(
            valor=200.00,
            dataEntrada=timezone.now(),
            dataSaida=timezone.now(),
            qntDatas=7,
            user=self.usuario  # Associando a reserva ao usuário criado acima
            # Aqui você precisa ajustar os outros campos conforme necessário
        )

    def test_criar_usuario(self):
        """ Testa a criação de um usuário """
        usuario = Usuario.objects.get(username='testeusuario')
        self.assertEqual(usuario.first_name, 'Teste')
        self.assertEqual(usuario.last_name, 'Usuário')
        self.assertEqual(usuario.email, 'teste@exemplo.com')
        self.assertEqual(usuario.cpf, '12345678900')
        self.assertEqual(usuario.celular, '(99) 99999-9999')
        self.assertEqual(usuario.endereco, 'Rua Exemplo, 123')

    def test_criar_reserva(self):
        """ Testa a criação de uma reserva """
        reserva = Reserva.objects.get(user=self.usuario)
        self.assertEqual(reserva.valor, 200.00)
        # Adicione mais verificações conforme necessário para outros campos da reserva

    def test_associacao_usuario_reserva(self):
        """ Testa a associação entre usuário e reserva """
        reserva = Reserva.objects.get(user=self.usuario)
        self.assertEqual(reserva.user, self.usuario)
