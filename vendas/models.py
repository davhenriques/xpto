from django.db import models

# Create your models here.
class Carrinho(models.Model):
    user_id = models.IntegerField()
    prod_id = models.IntegerField()
    quantidade = models.IntegerField()
    data = models.DateTimeField()

    def __str__(self):
        return self.nome


class Vendas(models.Model):
    user_id = models.IntegerField()
    data = models.DateTimeField()

    def __str__(self):
        return self.nome


class Vendas_Estado(models.Model):
    vendas_id = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    estado = models.IntegerField()
    data = models.DateTimeField()


class Vendas_Produtos(models.Model):
    vendas_id = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    prod_id = models.IntegerField()
    quantidade = models.IntegerField()

    def __str__(self):
        return self.nome


class Promocoes(models.Model):
    prod_id = models.IntegerField()
    percentagem = models.IntegerField()
    data_exp = models.DateTimeField()

    def __str__(self):
        return self.nome


class Prod_Stock_Preco(models.Model):
    prod_id = models.IntegerField()
    preco_base = models.DecimalField(decimal_places=2, max_digits=6)
    stock = models.IntegerField()
