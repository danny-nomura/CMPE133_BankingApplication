from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from .forms import CreateUserForm
from . import transactions
from .models import History, Account


def register_home(request):

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, "Email already exists.")
            else:
                form.save()
                user = User.objects.get(username=form.cleaned_data['username'])
                transactions.generate_account_number(user)
                return redirect("login")
        else:
            messages.error(request, form.errors)

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
        else:
            messages.error(request, "Invalid Username or Password")

    context = {}

    return render(request, 'users/login.html', context)


@login_required
def user_dashboard(request):
    account_number = Account.objects.get(user_id=request.user).account_number
    history = History.objects.filter(
        account_number=account_number).order_by('-datetime')
    balance = Account.objects.get(user_id=request.user).balance
    
    context = {
        'account_number' : account_number,
        'balance' : balance,
        'history': history,
    }
    return render(request, 'users/homepage_dashboard.html', context)


@login_required
def user_settings(request):
    if request.method == 'POST':
        if request.POST.get('email_button'):
            email = request.POST.get('email1')
            if email == request.POST.get('email2'):
                try:
                    validate_email(email)
                    request.user.email = email
                    request.user.save()
                    messages.info(request, "Successfully changed email!")
                except ValidationError:
                    messages.error(request, "Invalid email. Try again.")
            else:
                messages.error(request, "Invalid email. Try again.")
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


@login_required
def user_transfer(request):
    if request.method == 'POST':
        transactions.transfer(request)
    return render(request, 'users/homepage_transfer.html')


@login_required
def user_withdraw(request):
    if request.method == 'POST':
        transactions.withdraw(request)
    return render(request, 'users/homepage_withdraw.html')
