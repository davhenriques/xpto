# Generated by Django 4.1.5 on 2023-01-28 14:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("vendas", "0002_carrinho_data_carrinho_prod_id_carrinho_quantidade_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="Prod_Stock_Preco",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prod_id", models.IntegerField()),
                ("preco_base", models.DecimalField(decimal_places=2, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name="Promocoes",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prod_id", models.IntegerField()),
                ("percentagem", models.IntegerField()),
                ("data_exp", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Vendas",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("user_id", models.IntegerField()),
                ("data", models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name="Vendas_Produtos",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("prod_id", models.IntegerField()),
                ("quantidade", models.IntegerField()),
                (
                    "vendas_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vendas.vendas"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Vendas_Estado",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("estado", models.IntegerField()),
                ("data", models.DateTimeField()),
                (
                    "vendas_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="vendas.vendas"
                    ),
                ),
            ],
        ),
    ]
