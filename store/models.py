from django.db import models
from datetime import date


# Create your models here.

class User(models.Model):
    nome = models.CharField(max_length=100)

    def __str__(self):
        return self.nome


class Produtos(models.Model):
    comercial = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    preco = models.FloatField

    def __str__(self):
        return self.nome
