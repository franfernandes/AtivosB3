# Generated by Django 4.2.9 on 2024-01-12 17:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ativos', '0004_ativo_limiar_compra_ativo_limiar_venda_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ativo',
            name='limite_compra',
        ),
        migrations.RemoveField(
            model_name='ativo',
            name='limite_venda',
        ),
    ]
