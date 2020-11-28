from django.urls import path
from django.http import HttpResponse

from . import views


urlpatterns = [
    path('', views.register_home, name='register'),
    path('login/', views.login_home, name='login'),
    path('dashboard/', views.user_dashboard, name='Dashboard'),
]
