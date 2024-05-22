import json

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

class Apartamento(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
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
    
class Usuario(AbstractUser):
    cupons_utilizados = models.ManyToManyField(Cupons)

class Reserva(models.Model):
    valor = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    dataEntrada = models.DateTimeField(null=True, blank=True)
    dataSaida = models.DateTimeField(null=True, blank=True)
    qntDias = models.JSONField(null=True, blank=True)  # Campo JSONField para armazenar as datas
    user = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False)
    data_criacao = models.DateTimeField(default=timezone.now)
    cupons = models.ForeignKey(Cupons, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False)

    def save(self, *args, **kwargs):
        if self.dataEntrada and self.dataSaida:
            # Gerar lista de datas entre dataEntrada e dataSaida
            datas_entre = []
            current_date = self.dataEntrada
            while current_date <= self.dataSaida:
                datas_entre.append(current_date.date())
                current_date += timezone.timedelta(days=1)

            # Converter a lista de datas para lista de strings e armazenar em datas como JSON
            self.qntDias = ', '.join([str(date) for date in datas_entre])
        super(Reserva, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('administracao:reserva')






