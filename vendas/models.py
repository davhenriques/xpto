from django.db import models

# Create your models here.
class Carrinho(models.Model):
    user_id = models.IntegerField()
    prod_id = models.IntegerField()
    quantidade = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.nome


class Vendas(models.Model):
    user_id = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.nome


class Vendas_Estado(models.Model):
    vendas_id = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    estado = models.IntegerField()
    data = models.DateTimeField(auto_now_add=True, blank=True)


class Vendas_Produtos(models.Model):
    vendas_id = models.ForeignKey(Vendas, on_delete=models.CASCADE)
    prod_id = models.IntegerField()
    quantidade = models.IntegerField()

    def __str__(self):
        return self.nome


class Promocoes(models.Model):
    prod_id = models.IntegerField()
    percentagem = models.DecimalField(decimal_places=2, max_digits=5)
    data_exp = models.DateTimeField()

    def __str__(self):
        return self.nome


class Prod_Stock_Preco(models.Model):
    prod_id = models.IntegerField()
    preco_base = models.DecimalField(decimal_places=2, max_digits=6)
    stock = models.IntegerField()


class Carrinho_Preco(models.Model):
    id = models.BigIntegerField(primary_key=True)
    prod_id = models.IntegerField()
    user_id = models.IntegerField()
    preco_base = models.DecimalField(decimal_places=2, max_digits=6)
    quantidade = models.IntegerField()
    promotion = models.DecimalField(decimal_places=2, max_digits=6)
    preco_final = models.DecimalField(decimal_places=2, max_digits=6)

    class Meta:
        managed = False
        db_table = 'vendas_carrinho_preco'

