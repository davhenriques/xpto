from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cart', views.cart, name='cart'),
    path('checkout', views.checkout, name='checkout'),
    path('produtos', views.produtos, name='produtos'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register', views.register, name='register'),
    path('administrarcomerciais', views.administrarcomerciais, name='administrarcomerciais'),
    path('settings', views.settings, name='settings'),
    path('vendas', views.vendas, name='vendas'),
    path('vendasprods', views.vendasprods, name='vendasprods'),
    path('atividadecomerciais', views.atividadecomerciais, name='atividadecomerciais'),
    path('logs', views.logs, name='logs'),
]
