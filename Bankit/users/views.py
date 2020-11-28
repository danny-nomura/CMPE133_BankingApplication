from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm


from .forms import CreateUserForm
from . import transactions


def register_home(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

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


@login_required
def user_deposit(request):
    user = request.user
    if request.method == 'POST':
        if request.POST.get('amount') == request.POST.get('confirm_amount'):
            amount = request.POST.get('amount')
            account_to = request.POST.get('account_to')
            transactions.deposit(user, amount, account_to)
    return render(request, 'users/homepage_deposit.html')


@login_required
def user_transfer(request):
    user = request.user
    if request.method == 'POST':
        amount = request.POST.get('amount')
        account_from = request.POST.get('account_from')
        account_to = request.POST.get('account_to')
        transactions.transfer(user, amount, account_from, account_to)
    return render(request, 'users/homepage_transfer.html')


@login_required
def user_withdraw(request):
    user = request.user
    if request.method == 'POST':
        if request.POST.get('amount') == request.POST.get('confirm_amount'):
            amount = request.POST.get('amount')
            account_from = request.POST.get('account_from')
            transactions.withdraw(user, amount, account_from)
    return render(request, 'users/homepage_withdraw.html')

