# Generated by Django 5.0.6 on 2024-06-04 18:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracao', '0003_alter_usuario_cpf'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='celular',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='usuario',
            name='endereco',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
