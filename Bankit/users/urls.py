from django.urls import path
from django.http import HttpResponse

from . import views


urlpatterns = [
    path('', views.register_home, name='register'),
    path('login/', views.login_home, name='login'),
    path('logout', views.user_logout, name="logout"),
    path('dashboard/', views.user_dashboard, name='Dashboard'),
    path('settings/', views.user_settings, name='Settings'),
    path('deposit/', views.user_deposit, name='Deposit'),
    path('transfer/', views.user_transfer, name='Transfer'),
    path('withdraw/', views.user_withdraw, name='Withdraw'),
]
