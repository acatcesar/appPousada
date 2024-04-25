from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class Apartamento(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField
    numero = models.IntegerField(default=0)
    status = models.BooleanField(default=False)

    def __str__(self):
        return self.nome

class Cupons(models.Model):
    codigo = models.CharField(max_length=50)
    desconto = models.IntegerField(default=0)
    utilizado = models.IntegerField(default=0)

    def __str__(self):
        return self.codigo

class Reserva(models.Model):
    valor = models.DecimalField
    dataEntrada= models.DateTimeField
    dataSaida = models.DateTimeField
    qntDias = models.IntegerField(default=0)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, null=True, blank=True)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False)
    data_criacao = models.DateTimeField(default=timezone.now)
    cupons = models.ForeignKey(Cupons, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False)



class Usuario(AbstractUser):
    cupons_utilizados = models.ManyToManyField(Cupons)




