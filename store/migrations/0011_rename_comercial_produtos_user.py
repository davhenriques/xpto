# Generated by Django 4.1.5 on 2023-02-01 19:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0010_produtos_estado"),
    ]

    operations = [
        migrations.RenameField(
            model_name="produtos", old_name="comercial", new_name="user",
        ),
    ]