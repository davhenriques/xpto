from django.shortcuts import render, redirect, HttpResponse, Http404
from django.core.paginator import Paginator
from django.template.response import TemplateResponse
from djongo.database import IntegrityError, DatabaseError
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from store.models import *
from django.db.models import Q
from vendas.models import *
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from decimal import Decimal
from django.db import connections
from django.core.files.storage import FileSystemStorage
import uuid
from django.core import serializers
import json

# tests
def isAdmin(user):
    return 'admin' in list(user.groups.values_list('name', flat=True))


def isComercial1(user):
    print(list(user.groups.values_list('name', flat=True)))
    return 'Comercial Administrador' in list(user.groups.values_list('name', flat=True))


def isComercial2(user):
    return 'Comercial Supervisor' in list(user.groups.values_list('name', flat=True))


def isParceiro(user):
    return 'Parceiro' in list(user.groups.values_list('name', flat=True))


def isComprador(user):
    return 'Comprador' in list(user.groups.values_list('name', flat=True))


def getHomePase(user):
    if isComprador(user):
        return ''
    if isParceiro(user) or isComercial2(user) or isComercial1(user):
        return '/produtos'
    if isAdmin(user):
        return '/administrarcomerciais'


# views
def index(request):
    # se o utilizador não é cliente deve ser redirecionado para a página correta
    if request.user.is_authenticated:
        if 'Comprador' not in list(request.user.groups.values_list('name', flat=True)):
            # print("getHomePase(request.user)={" + getHomePase(request.user) + "}")
            # print(getHomePase(request.user))
            return redirect(getHomePase(request.user))
    # get recomendados
    try:
        recomendados_raw = Vendas_Produtos.objects.raw(
            'select vp.prod_id as "id", count(vp.prod_id) from vendas_vendas_produtos as vp '
            'left join vendas_prod_stock_preco as psp on vp.prod_id = psp.prod_id '
            'where psp.stock > 0 '
            'group by vp.prod_id '
            'order by count(vp.prod_id) desc limit 4;')
    except Exception as e:
        print(e)
    recomendados = []
    for rec in recomendados_raw:
        try:
            recomendados.append({'Produto': Produtos.objects.get(id=rec.id, estado='ativo'),
                                 'pspp': Produtos_Stock_Preco_Prom.objects.get(prod_id=rec.id)})
        except Exception as e:
            print(e)
    prods = []
    # get produtos listagem
    try:
        _prods = Produtos_Stock_Preco_Prom.objects.all()
        for p in _prods:
            try:
                if request.method == 'GET' and 'filter' in request.GET:
                    aux = Produtos.objects.get(id=p.prod_id, tipo=request.GET['filter'], estado='ativo')
                else:
                    aux = Produtos.objects.get(id=p.prod_id, estado='ativo')
                prods.append({'Produto': aux, 'pspp': p})
            except Exception as e:
                print(e)
    except Exception as e:
        print(e)

    # get tipo de produto

    paginator = Paginator(prods, 24)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj': page_obj, 'recomendados': recomendados}
    if request.method == 'GET':
        return render(request, "index.html", context)
    if request.method == 'POST':
        try:
            if request.user.is_authenticated:
                print("request.user.is_authenticated")
                carrinho = Carrinho.objects.create(user_id=request.user.id,
                                                   prod_id=request.POST['id'],
                                                   quantidade=1)
            else:
                print("request.session.session_key")
                carrinho = Carrinho.objects.create(session_id=request.session.session_key,
                                                   prod_id=request.POST['id'],
                                                   quantidade=1)
            carrinho.save()
        except Exception as e:
            print("Exception")
            print(e)
        return render(request, "index.html", context)


def cart(request):
    if request.user.is_authenticated:
        if 'Comprador' not in list(request.user.groups.values_list('name', flat=True)):
            redirect(getHomePase(request.user))
    if request.method == 'POST':
        if 'id' in request.POST:
            if request.POST['action'] == 'alterar_quantidade':
                try:
                    cart = Carrinho.objects.get(id=request.POST['id'])
                    cart.quantidade = request.POST['quantidade']
                    cart.save()
                except Exception as e:
                    messages.error(request, "quantidade selecionada excede limite")
                    print(e)
                print('sucesso a alterar a quantiade')
            if request.POST['action'] == 'delete':
                try:
                    cart = Carrinho.objects.get(id=request.POST['id'])
                    cart.delete()
                except Exception as e:
                    print(e)
        if request.POST['action'] == 'finalizar_compra':
            if not request.user.is_authenticated:
                print("user no authenticated")
                return redirect('/register/?next=/produtos')
            try:
                cursor = connections['vendas_psgl'].cursor()
                cursor.execute("CALL finalizarcompra(%s);", [request.user.id])
                return redirect('/logs')
            except Exception as e:
                print("deu erro!")
                print(e)
    if request.user.is_authenticated:
        _cart = Carrinho_Preco.objects.filter(user_id=request.user.id)
    else:
        _cart = Carrinho_Preco.objects.filter(session_id=request.session.session_key)
    # estados = Estados.objects.all()
    cart = []
    for item in _cart:
        p = Produtos.objects.get(id=item.prod_id)
        cart.append({'cart': item, 'produto': p})
    context = {'cart': cart}
    return render(request, "cart.html", context)


@user_passes_test(isComprador)
def checkout(request):
    return render(request, "checkout.html")


@user_passes_test(lambda u: isComercial1(u) or isComercial2(u) or isParceiro(u))
def produtos(request):
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

        if request.POST.get('action') == 'ativar':
            try:
                print(request.POST['ativo'])
                Produtos.objects.filter(id=request.POST['id']).update(estado=request.POST['ativo'])
                try:
                    atividade = AtividadeComerciais.objects.create(user=request.user, acao='Atualizar Produto com id:'
                                                                                           + request.POST['id']
                                                                                           + ' para estado:' +
                                                                                           request.POST['ativo'])
                    atividade.save()
                except Exception as e:
                    print(e)
            except Exception as e:
                print(e)
        if request.POST.get('action') == 'create':
            myfile = request.FILES['img_url']
            fs = FileSystemStorage()
            filename = fs.save(str(uuid.uuid4()) + ".png", myfile)
            uploaded_file_url = fs.url(filename)
            try:
                p = Produtos.objects.create(user_id=request.user.id,
                                            nome=request.POST['nome'],
                                            descricao=request.POST['descricao'],
                                            tipo=request.POST['tipo'],
                                            parceiro=request.POST['parceiro'],
                                            img_url=uploaded_file_url)
                p.save()
                try:
                    pstockprice = Prod_Stock_Preco.objects.create(prod_id=p.id,
                                                                  preco_base=request.POST['precobase'],
                                                                  stock=request.POST['stock'])
                    pstockprice.save()
                    pprom = Promocoes.objects.create(prod_id=p.id,
                                                     percentagem=0)
                    pprom.save()
                    try:
                        atividade = AtividadeComerciais.objects.create(user=request.user,
                                                                       acao='Criar Produto com id:' + p.id)
                        atividade.save()
                    except Exception as e:
                        print(e)
                except:
                    p.delete()
            except Exception as e:
                print(e)
        if request.POST.get('action') == 'delete':
            if request.POST['id'] is not None:
                try:
                    Produtos.objects.get(id=request.POST['id']).delete()
                    Prod_Stock_Preco.objects.get(prod_id=request.POST['id']).delete()
                    Carrinho.objects.get(prod_id=request.POST['id']).delete()
                    try:
                        atividade = AtividadeComerciais.objects.create(user=request.user,
                                                                       acao='Apagar Produto com id:' + request.POST['id'])
                        atividade.save()
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
        if request.POST.get('action') == 'promotion':
            if request.POST['id'] is not None:
                try:
                    prom = Promocoes.objects.get(prod_id=request.POST['id'])
                    prom.percentagem = float(request.POST['promotion'])
                    prom.data_exp = request.POST['validade']
                    prom.save()
                    try:
                        atividade = AtividadeComerciais.objects.create(user=request.user,
                                                                       acao='Adicionar promocao ao  Produto com id:'
                                                                            + request.POST['id']
                                                                            + " para desconto:" + request.POST['promotion']
                                                                            + "com validade até" + request.POST['validade']
                                                                        )
                        atividade.save()
                    except Exception as e:
                        print(e)
                except Exception as e:
                    print(e)
    prods = []
    try:
        if isParceiro(request.user):
            _prods = Produtos.objects.filter(user_id=request.user.id)
        else:
            _prods = Produtos.objects.all()
        for p in _prods:
            pspp = Produtos_Stock_Preco_Prom.objects.get(prod_id=p.id)
            prods.append({'Produto': p, 'pspp': pspp})
    except Exception as e:
        print(e)
    context = {"prods": prods}
    if request.method == 'GET' and 'action' in request.GET and request.GET['action'] == 'xml':
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        xml_serializer.serialize(_prods)
        dataProds = xml_serializer.getvalue()
        XMLSerializer = serializers.get_serializer("xml")
        xml_serializer = XMLSerializer()
        xml_serializer.serialize(Produtos_Stock_Preco_Prom.objects.all())
        dataProdsSql = xml_serializer.getvalue()
        context['xml'] = {'sql': dataProdsSql, 'mongo': dataProds}
        # print(list(xml))
    if request.method == 'GET' and 'action' in request.GET and request.GET['action'] == 'json':
        prodsjson = serializers.serialize('json', _prods)
        psppjson = serializers.serialize('json', Produtos_Stock_Preco_Prom.objects.all())
        context['json'] = {'sql': psppjson, 'mongo': prodsjson}
    if request.method == 'GET':
        req_id = request.GET.get('id')
        if req_id is not None:
            try:
                req_prod = Produtos.objects.get(id=req_id)
                req_prod_ar = []
                req_pspp = Produtos_Stock_Preco_Prom.objects.get(prod_id=req_id)
                req_prod_ar.append({'Produto': req_prod, 'pspp': req_pspp})
                context['req_prod'] = req_prod_ar
            except:
                print("No product found with id ={" + req_id + "}")
            print(context)
        return TemplateResponse(request, "produtos.html", context)

    return TemplateResponse(request, "produtos.html", context)


@user_passes_test(lambda u: isAdmin(u))
def administrarcomerciais(request):
    coms = User.objects.filter(
        Q(groups__name='Comercial Administrador') | Q(groups__name='Comercial Supervisor') | Q(groups__name='Parceiro'))
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
                Carrinho.objects.filter(session_id=request.session.session_key).update(user_id=user.id)
        return render(request, '../templates/registration/login.html')
    groups = Group.objects.all()
    context = {"groups": groups}
    return render(request, 'register.html', context)


@login_required(login_url="/accounts/login/")
def settings(request):
    if request.method == 'POST':
        if request.POST['action'] == 'nome':
            try:
                user = User.objects.get(id=request.user.id)
                user.first_name = first_name = request.POST['nome']
                user.last_name = last_name = request.POST['sobrenome']
            except Exception as e:
                print(e)
            if request.POST['action'] == 'nome':
                try:
                    user = User.objects.get(id=request.user.id)
                    user.first_name = first_name = request.POST['nome']
                    user.last_name = last_name = request.POST['sobrenome']
                except Exception as e:
                    print(e)
    return render(request, 'settings.html')


@user_passes_test(isComprador)
def logs(request):
    if request.method == 'POST':
        try:
            cursor = connections['vendas_psgl'].cursor()
            cursor.execute("CALL cancelarcompra(%s);", [request.POST['id']])
        except Exception as e:
            print(e)
        print(request.POST['action'])
        print(request.POST['id'])

    vendas = Vendas.objects.raw(
        "Select * from vendas_vendas as v  inner join vendas_vendas_estado as ve on v.id = ve.vendas_id_id and ve.id in (Select id from vendas_vendas_estado where vendas_vendas_estado.vendas_id_id=v.id order by data desc limit 1) inner join vendas_estados as est on ve.estado_id = est.id where user_id=" + str(
            request.user.id) + " order by ve.data, ve.id desc")
    print(vendas)
    context = {'vendas': vendas}
    return render(request, 'logs.html', context)


@user_passes_test(lambda u: isComercial1(u) or isComercial2(u) or isParceiro(u))
def vendas(request):
    # delete
    if request.method == 'POST' and request.POST['action'] == 'delete':
        try:
            cursor = connections['vendas_psgl'].cursor()
            cursor.execute("CALL cancelarcompra(%s);", [request.POST['id']])
            try:
                atividade = AtividadeComerciais.objects.create(user=request.user,
                                                               acao='Delete Venda com id:' + request.POST['id'])
                atividade.save()
            except Exception as e:
                print(e)
        except Exception as e:
            print(e)
    #     update estado
    if request.method == 'POST' and request.POST['action'] == 'nextstate':
        try:
            print(request.POST['estado'])
            v_est = Vendas_Estado.objects.create(vendas_id=Vendas.objects.get(id=request.POST['id']),
                                                 estado_id=request.POST['estado'])
            v_est.save()
            try:
                atividade = AtividadeComerciais.objects.create(user=request.user, acao='Atualizar Venda com id:'
                                                                                       + request.POST['id']
                                                                                       + ' para estado:' +
                                                                                       request.POST['estado'])
                atividade.save()
            except Exception as e:
                print(e)
        except Exception as e:
            print("Exception")
            print(e)

    vendas = Vendas.objects.raw(
        "Select * from vendas_vendas as v  "
        "inner join vendas_vendas_estado as ve on v.id = ve.vendas_id_id "
        "and ve.id in (Select id from vendas_vendas_estado where vendas_vendas_estado.vendas_id_id=v.id order by data desc limit 1) "
        "inner join vendas_estados as est on ve.estado_id = est.id order by ve.data, ve.id desc")

    estados = Estados.objects.all()
    context = {'vendas': vendas, 'estados': estados}
    return render(request, 'vendas.html', context)


@user_passes_test(lambda u: isComercial1(u) or isComercial2(u) or isParceiro(u))
def vendasprods(request):
    filtro = ''
    if request.method == 'POST':
        filtro = request.POST['produtonome']
    print(filtro)
    vendas = Vendas_Produtos.objects.all().order_by('-vendas_id_id')
    prodven = []
    for v in vendas:
        try:
            if filtro == '':
                prodven.append({'vendaprod': v, "venda": Vendas.objects.get(id=v.vendas_id_id),
                                'produto': Produtos.objects.get(id=v.prod_id)})
            else:
                prodven.append({'vendaprod': v, "venda": Vendas.objects.get(id=v.vendas_id_id),
                                'produto': Produtos.objects.get(id=v.prod_id, nome__contains=filtro)})

        except Exception as e:
            print(e)
    context = {'vendas': prodven}
    return render(request, 'vendasprod.html', context)


@user_passes_test(lambda u: isComercial2(u))
def atividadecomerciais(request):
    filtro = ''
    if request.method == 'POST':
        filtro = request.POST['nome']

    try:
        atividadecomerciais = AtividadeComerciais.objects.filter(user=User.objects.get(username__contains=filtro))
        context = {'atividade': atividadecomerciais}
    except Exception as e:
        context = {'atividade': {}}

    return render(request, 'atividadecomerciais.html', context)
