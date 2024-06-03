# Generated by Django 5.0.6 on 2024-05-23 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('administracao', '0003_alter_cupons_codigo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupons',
            name='codigo',
            field=models.CharField(blank=True, max_length=6, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='cupons',
            name='utilizado',
            field=models.BooleanField(default=False),
        ),
    ]