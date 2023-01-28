from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.


class Produtos(models.Model):
    comercial = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=512)

    def __str__(self):
        return self.nome
