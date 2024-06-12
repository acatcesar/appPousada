import json
import random
import string
from datetime import datetime
from sqlalchemy.sql.functions import user
from datetime import timedelta, date

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse
from cpf_field.models import CPFField

class Apartamento(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(default=0.0, max_digits=10, decimal_places=2)
    numero = models.IntegerField(default=0)
    status = models.BooleanField(default=False)
    qntDias = models.JSONField(null=True, blank=True)
    foto = models.ImageField(upload_to='fotos_apartamento')

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
    cpf = CPFField('cpf')
    celular = models.CharField(max_length=20, null=True, blank=True)
    endereco = models.CharField(max_length=100, null=True, blank=True)

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

    def save(self, *args, **kwargs):
        # Salva a reserva
        super().save(*args, **kwargs)



        if self.apartamento and self.qntDias:

            datas_exist = self.apartamento.qntDias.split(", ") if self.apartamento.qntDias else []
            data_atual = self.dataEntrada
            data_final = self.dataSaida
            datas_novas = []
            while data_atual <= data_final:
                data_str = data_atual.strftime('%d-%m-%Y')
                if data_str not in datas_exist:
                    datas_novas.append(data_str)
                data_atual += timedelta(days=1)

            datas_exist.extend(datas_novas)

            self.apartamento.qntDias = ", ".join(datas_exist)
            self.apartamento.save()

    def get_absolute_url(self):
        return reverse('administracao:reserva')






