from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from djongo.database import IntegrityError, DatabaseError
from store.models import Produtos
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test


# tests
def isAdmin(user):
    return 'admin' in list(user.groups.values_list('name', flat=True))


def isComercial1(user):
    print(list(user.groups.values_list('name', flat=True)))
    return 'Comercial Administrador' in list(user.groups.values_list('name', flat=True))


def isComercial2(user):
    return 'Comercial Supervisionador' in list(user.groups.values_list('name', flat=True))


def isParceiro(user):
    return 'Parceiro' in list(user.groups.values_list('name', flat=True))


def isComprador(user):
    return 'Comprador' in list(user.groups.values_list('name', flat=True))


# views
def index(request):
    if request.method == 'GET':
        prods = Produtos.objects.all()
        print(prods)
        context = {"prods": prods}
        return TemplateResponse(request, "index.html", context)


@user_passes_test(isComercial1)
def cart(request):
    return render(request, "cart.html")


@user_passes_test(isComprador)
def checkout(request):
    return render(request, "checkout.html")


@user_passes_test(lambda u: isComercial1(u) or isComercial2(u))
def produtos(request):
    p = Produtos(comercial=request.user, nome='teste', precobase=12.25, descricao="abcedfg")
    p.save()
    return render(request, 'produtos.html')


def register(request):
    if request.method == 'POST':
        print('request.POST')
        print(request.POST)
        if request.POST['email'] == '' or request.POST['username'] == '' or request.POST['password'] == '' or '' == \
                request.POST['group']:
            messages.error(request, "Campos em branco")
            return redirect('/register')
        try:
            obj = User.objects.get(username=request.POST['username'])
            messages.error(request, "username já existe")
            return redirect('/register')
        except User.DoesNotExist:
            try:
                obj = User.objects.get(email=request.POST['email'])
                messages.error(request, "email já associado a uma conta")
                return redirect('/register')
            except User.DoesNotExist:
                print("teste")
                user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password'])
                group = Group.objects.get(name=request.POST['group'])
                user.save()
                group.user_set.add(user)
        return render(request, '../templates/registration/login.html')
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, 'register.html', context)
