from django.shortcuts import render
from django.template.response import TemplateResponse
from store.models import Produtos, User


# Create your views here.
def index(request):
    if request.method == 'GET':
        prods = Produtos.objects.all()
        context = {"prods": prods}
        return TemplateResponse(request, "index.html", context)


def cart(request):
    return render(request, "cart.html")


def checkout(request):
    return render(request, "checkout.html")

def produto(request):
    return render(request, 'produto.html')
