from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from djongo.database import IntegrityError, DatabaseError
from store.models import Produtos
from django.db.models import Q
from vendas.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from decimal import Decimal


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
        context = {"prods": prods}
        return TemplateResponse(request, 'index.html', context)


@user_passes_test(isComercial1)
def cart(request):
    return render(request, "cart.html")


@user_passes_test(isComprador)
def checkout(request):
    return render(request, "checkout.html")


@user_passes_test(lambda u: isComercial1(u) or isComercial2(u))
def produtos(request):
    _prods = Produtos.objects.all()
    prods = []
    i = 0
    for p in _prods:
        try:
            psp = Prod_Stock_Preco.objects.get(prod_id=p.id)
            prods.append({'id': p.id, 'descricao': p.descricao, 'nome': p.nome, 'preco_base': psp.preco_base, 'stock': psp.stock})
        except Exception as e:
            print("except")
            print(e)

    context = {"prods": prods}
    if request.method == 'GET':
        req_id = request.GET.get('id')
        if req_id is not None:
            try:
                req_prod = Produtos.objects.get(id=req_id)
                req_prod_ar = []
                req_psp = Prod_Stock_Preco.objects.get(prod_id=p.id)
                req_prod_ar.append({'id': req_prod.id, 'descricao': req_prod.descricao, 'nome': req_prod.nome, 'preco_base': req_psp.preco_base, 'stock': req_psp.stock})
                context['req_prod'] = req_prod_ar
            except:
                print("No product found with id ={" + req_id + "}")
            print(context)
        return TemplateResponse(request, "produtos.html", context)
    if request.method == 'POST':
        if request.POST.get('action') == 'edit':
            try:
                if request.POST.get('nome') is not None and request.POST.get(
                        'descricao') is not None and request.POST.get('precobase') is not None:
                    Produtos.objects.filter(id=request.POST['id']).update(nome=request.POST['nome'],
                                                                          descricao=request.POST['descricao'])
                    Prod_Stock_Preco.objects. \
                        filter(prod_id=request.POST['id']). \
                        update(preco_base=request.POST['precobase'],
                               stock=request.POST['stock'])
            except Exception as e:
                print(e)

        if request.POST.get('action') == 'create':
            try:
                p = Produtos.objects.create(comercial_id=request.user.id,
                                            nome=request.POST['nome'],
                                            descricao=request.POST['descricao'])
                p.save()
                try:
                    pstockprice = Prod_Stock_Preco.objects.create(prod_id=p.id,
                                                                  preco_base=request.POST['precobase'],
                                                                  stock=request.POST['stock'])
                except:
                    p.delete()
            except Exception as e:
                print(e)
        if request.POST.get('action') == 'delete':
            if request.POST['id'] is not None:
                try:
                    Produtos.objects.get(id=request.POST['id']).delete()
                    Prod_Stock_Preco.objects.get(prod_id=request.POST['id']).delete()
                except Exception as e:
                    print(e)
    return TemplateResponse(request, "produtos.html", context)


@user_passes_test(lambda u: isAdmin(u))
def administrarcomerciais(request):
    coms = User.objects.filter(Q(groups__name='Comercial Administrador') | Q(groups__name='Comercial Supervisor'))
    context = {"coms": coms}
    if request.method == 'POST' and request.POST['id'] is not None:
        if request.POST['action'] == 'delete':
            try:
                User.objects.filter(id=request.POST['id']).delete()
            except Exception as e:
                print(e)
        if request.POST['action'] == 'inactivate':
            try:
                User.objects.filter(id=request.POST['id']).update(is_active=False)
            except Exception as e:
                print(e)
        if request.POST['action'] == 'activate':
            try:
                User.objects.filter(id=request.POST['id']).update(is_active=True)
            except Exception as e:
                print(e)

    return TemplateResponse(request, "administrarusers.html", context)


def register(request):
    if request.method == 'POST':
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
                user = User.objects.create_user(request.POST['username'], request.POST['email'],
                                                request.POST['password'],
                                                is_active=True if request.POST['group'] == 'Comprador' else False)
                group = Group.objects.get(name=request.POST['group'])
                user.save()
                group.user_set.add(user)
        return render(request, '../templates/registration/login.html')
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, 'register.html', context)


def home(request):
    _prods = Produtos.objects.all()
    prods = []
    i = 0
    for p in _prods:
        try:
            psp = Prod_Stock_Preco.objects.get(prod_id=p.id)
            print(psp)
        except Exception as e:
            print(e)
        prods.append({'descricao': p.descricao, 'nome': p.nome, 'preco_base': psp.preco_base, 'stock': psp.stock})
    print(prods)
    context = {"prods": prods}
    print("context: " + str(context))
    return TemplateResponse(request, "body.html", context)



