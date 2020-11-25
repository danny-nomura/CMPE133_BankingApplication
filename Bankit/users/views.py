
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import authenticate, login, logout

from django.contrib import messages


# Create your views here.
from .forms import CreateUserForm
from .models import *
from django.contrib.auth.decorators import login_required


def registerHome(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required
def User_Dashboard(request):

    return render(request, 'users/dashboard.html')


def loginHome(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("Dashboard")

    context = {}

    return render(request, 'users/login.html', context)
