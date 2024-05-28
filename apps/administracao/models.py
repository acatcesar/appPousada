import json
import random
import string
from datetime import datetime

from datetime import timedelta, date

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
    qntDias = models.JSONField(null=True, blank=True)




    def __str__(self):
        return self.nome

class Cupons(models.Model):
    codigo = models.CharField(max_length=6, unique=True, null=True, blank=True)
    desconto = models.IntegerField(default=0)
    utilizado = models.BooleanField(default=False)

    def __str__(self):
        return self.codigo

    def save(self, *args, **kwargs):
        if not self.codigo:
            # Gera um código aleatório de 6 caracteres
            self.codigo = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        super().save(*args, **kwargs)
    
class Usuario(AbstractUser):
    cupons_utilizados = models.ManyToManyField(Cupons)

class Reserva(models.Model):
    valor = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    dataEntrada = models.DateTimeField(null=True, blank=True)
    dataSaida = models.DateTimeField(null=True, blank=True)
    qntDias = models.JSONField(null=True, blank=True)
    qntDatas = models.IntegerField(default=0)
    user = models.ForeignKey(Usuario, on_delete=models.PROTECT, null=True, blank=True)
    apartamento = models.ForeignKey(Apartamento, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False)
    data_criacao = models.DateTimeField(default=timezone.now)
    cupons = models.ForeignKey(Cupons, on_delete=models.PROTECT, null=True, blank=True, db_constraint=False)

    # def save(self, *args, **kwargs):
    #     # Salva a reserva
    #     super().save(*args, **kwargs)

    def save(self, *args, **kwargs):
        # Salva a reserva
        super().save(*args, **kwargs)

        if self.apartamento and self.qntDias:
            # Recupera as datas existentes do apartamento
            datas_exist = self.apartamento.qntDias.split(", ") if self.apartamento.qntDias else []

            # Converte a sequência de dias em datas no formato "YYYY-MM-DD"
            data_atual = self.dataEntrada
            data_final = self.dataSaida
            datas_novas = []
            while data_atual <= data_final:
                data_str = data_atual.strftime('%Y-%m-%d')
                if data_str not in datas_exist:
                    datas_novas.append(data_str)
                data_atual += timedelta(days=1)

            # Adiciona as novas datas às existentes
            datas_exist.extend(datas_novas)

            # Salva a string de datas atualizada no apartamento
            self.apartamento.qntDias = ", ".join(datas_exist)
            self.apartamento.save()

    def get_absolute_url(self):
        return reverse('administracao:reserva')






