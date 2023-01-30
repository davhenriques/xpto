# Generated by Django 4.1.5 on 2023-01-30 18:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("vendas", "0003_alter_promocoes_percentagem"),
    ]

    operations = [
        migrations.CreateModel(
            name="Carrinho_Preco",
            fields=[
                ("id", models.BigIntegerField(primary_key=True, serialize=False)),
                ("prod_id", models.IntegerField()),
                ("quantidade", models.IntegerField()),
                ("promotion", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
            options={"db_table": "vendas_carrinho_preco", "managed": False,},
        ),
    ]
