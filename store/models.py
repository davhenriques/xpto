from django.db import models
from django.contrib.auth.models import User
from datetime import date


# Create your models here.

# class ProdutosInfo(models.Model):
#     nome = models.CharField(max_length=100)
#     descricao = models.CharField(max_length=512)
#     tipo = models.CharField(max_length=100)
#     estado = models.CharField(max_length=100, default='ativo')
#     img_url = models.CharField(max_length=100)
#
#     class Meta:
#         managed = False
#         db_table = 'store_produtosInfo'
    # def __str__(self):
    #     return self.nome


class Produtos(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=100)
    descricao = models.CharField(max_length=512)
    tipo = models.CharField(max_length=100)
    estado = models.CharField(max_length=100, default='ativo')
    img_url = models.CharField(max_length=100)
    parceiro = models.IntegerField(default=0)
    def __str__(self):
        return self.nome


