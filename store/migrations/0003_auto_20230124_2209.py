# Generated by Django 3.0.3 on 2023-01-24 22:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0002_auto_20230124_2154'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produtos',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
