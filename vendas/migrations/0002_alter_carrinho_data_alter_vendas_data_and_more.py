# Generated by Django 4.1.5 on 2023-01-28 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendas", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="carrinho",
            name="data",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="vendas",
            name="data",
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name="vendas_estado",
            name="data",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
