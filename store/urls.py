from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('produtos', views.produtos, name='produtos'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('home', views.home, name='home'),
    path('administrarcomerciais', views.administrarcomerciais, name='administrarcomerciais'),
]
