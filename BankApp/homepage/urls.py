from django.contrib import admin
from django.urls import path
from .views import Home, About,Login,Signup,Logout,create_account,account_list,deposit,withdraw,balance
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', Home, name="home"),
    path('about', About, name="about"),
    path('login', Login,name="login"),
    path('signup', Signup,name='signup'),
    path('logout', Logout,name='logout'),
    path('account', create_account,name='account'),
    path('account_list', account_list, name='account_list'),
    path("deposit/<str:account_number>", deposit, name='deposit'),
    path("withdraw/<str:account_number>", withdraw, name='withdraw'),
    path("balance/<str:account_number>", balance, name='balance'),
]