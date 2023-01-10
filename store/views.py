from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from store.models import Produtos, User
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


def UserLogin(request):
    if request.method == "POST":
        print("POST LOGIN")
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Successfully Logged In")
            return redirect("/")
        else:
            messages.error(request, "Invalid Credentials!!!" + username)
        alert = True
        return render(request, 'login.html', {'alert': alert})
    return render(request, "login.html")
