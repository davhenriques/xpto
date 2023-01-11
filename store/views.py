from django.shortcuts import render, redirect, HttpResponse, Http404
from django.template.response import TemplateResponse
from store.models import Produtos, User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProfileForm


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


def UserRegister(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if len(username) > 15:
            messages.error(request, "Username must be under 15 characters.")
            return redirect('/register')
        if not username.isalnum():
            messages.error(request, "Username must contain only letters and numbers.")
            return redirect('/register')
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('/register')

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()
        profile = Profile(user=user)
        profile.save()
        return render(request, 'login.html')
    return render(request, "register.html")

def UserLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect('/login')

@login_required(login_url = '/login')
def myprofile(request):
    if request.method=="POST":
        user = request.user
        profile = Profile(user=user)
        profile.save()
        form = ProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            obj = form.instance
            return render(request, "profile.html",{'obj':obj})
    else:
        form=ProfileForm()
    return render(request, "profile.html", {'form':form})


