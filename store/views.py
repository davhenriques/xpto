from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from store.models import Produtos
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# Create your views here.
def index(request):
    print("teste")
    if (request.user.is_anonymous):
        print("no login")
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


def register(request):
    if request.method == 'POST':
        print('request.POST')
        print(request.POST)
        if request.POST['email'] == '' or request.POST['username'] == '' or request.POST['password'] == '' or '' == \
                request.POST['group']:
            messages.error(request, "Campos em branco")
            return redirect('/register')
        user = User.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password'])
        group = Group.objects.get(name=request.POST['group'])
        user.save()
        group.user_set.add(user)
        return render(request, '../templates/registration/login.html')
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, 'register.html', context)
