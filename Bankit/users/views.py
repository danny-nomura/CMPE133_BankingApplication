from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .forms import CreateUserForm
from . import transactions


def register_home(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = User.objects.get(username=form.cleaned_data['username'])
            transactions.generate_account_number(user)
            return redirect("login")
        else:
            print(form.errors)

    context = {'form': form}
    return render(request, 'users/register.html', context)


def login_home(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("Dashboard")

    context = {}

    return render(request, 'users/login.html', context)


@login_required
def user_dashboard(request):
    return render(request, 'users/homepage_dashboard.html')


@login_required
def user_settings(request):
    return render(request, 'users/homepage_settings.html')


def user_logout(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("login")


@login_required
def user_deposit(request):
    if request.method == 'POST':
        transactions.deposit(request)
        return render(request, 'users/homepage_deposit.html')
    return render(request, 'users/homepage_deposit.html')


@login_required
def user_transfer(request):
    if request.method == 'POST':
        transactions.transfer(request)
        return render(request, 'users/homepage_transfer.html')
    return render(request, 'users/homepage_transfer.html')


@login_required
def user_withdraw(request):
    if request.method == 'POST':
        transactions.withdraw(request)
        return render(request, 'users/homepage_withdraw.html')
    return render(request, 'users/homepage_withdraw.html')

