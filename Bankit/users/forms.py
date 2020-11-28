from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name',
                  'email', 'password1', 'password2']

"""
class DepositForm(forms.Form):
    class Meta:
        fields = ['account_to', 'amount', 'confirm_amount']


class TransferForm(forms.Form):
    class Meta:
        fields = ['account_from', 'account_to', 'amount']


class WithdrawForm(forms.Form):
    class Meta:
        fields = ['account_from', 'amount', 'confirm_amount']
"""