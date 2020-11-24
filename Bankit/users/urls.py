
from django.urls import path


from django.http import HttpResponse
from. import views

urlpatterns = [

    path('', views.registerHome, name='register'),
    path('login/', views.loginHome, name='login'),
    path('dashboard/', views.User_Dashboard, name='Dashboard')


]
