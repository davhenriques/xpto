# Generated by Django 4.1.5 on 2023-01-28 16:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("store", "0007_produtos_precobase"),
    ]

    operations = [
        migrations.RemoveField(model_name="produtos", name="precobase",),
    ]
