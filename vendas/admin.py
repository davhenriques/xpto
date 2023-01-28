from django.contrib import admin
from store.models import *
from vendas.models import *
# Register your models here.

admin.site.register(Produtos)


admin.site.register(Vendas_Produtos)
admin.site.register(Prod_Stock_Preco)
