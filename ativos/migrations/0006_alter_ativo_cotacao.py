# Generated by Django 4.2.9 on 2024-01-12 20:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ativos', '0005_remove_ativo_limite_compra_remove_ativo_limite_venda'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ativo',
            name='cotacao',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
    ]