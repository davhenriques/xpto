# Generated by Django 4.1.5 on 2023-01-31 23:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendas", "0004_carrinho_preco"),
    ]

    operations = [
        migrations.AddField(
            model_name="carrinho",
            name="session_id",
            field=models.CharField(default="", max_length=100),
            preserve_default=False,
        ),
    ]
