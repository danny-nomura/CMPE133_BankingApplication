import random
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

from .models import Account, History


def transfer(request):
    account_to = None
    account_from = None
    amount = Decimal(request.POST.get('amount'))
    error = False

    try:
        account_from = Account.objects.get(account_number=request.POST.get('account_from'))
    except ObjectDoesNotExist:
        messages.error(request, "Account {} not found."
            .format(request.POST.get('account_from')))
        return
    try:
        account_to = Account.objects.get(account_number=request.POST.get('account_to'))
    except ObjectDoesNotExist:
        messages.error(request, "Account {} not found."
            .format(request.POST.get('account_to')))
        return
    if account_from.balance < amount:
        messages.error(request, "Your balance is too low.")
        error = True
    if account_from.user_id != request.user:
        messages.error(request, "You don't own the account from.")
        error = True
    if not error:
        account_from.balance -= amount
        account_to.balance += amount
        account_from.save()
        account_to.save()
        new_transaction_from = History(
            account_number=account_from, 
            transaction_type="T",
            amount=amount*-1,
            description="Transferred to {}"
                .format(mask_account_number(account_to.account_number)),
        )
        new_transaction_to = History(
            account_number=account_to, 
            transaction_type="T",
            amount=amount*-1,
            description="Transferred from {}"
                .format(mask_account_number(account_from.account_number)),
        )
        new_transaction_from.save()
        new_transaction_to.save()
        messages.success(request, "Successfully transfered ${} from account {} to account {}."
            .format(amount, mask_account_number(account_from.account_number), mask_account_number(account_to.account_number)))

def deposit(request):
    account_to = None
    amount = Decimal(request.POST.get('amount'))
    error = False
    
    try:
        account_to = Account.objects.get(account_number=request.POST.get('account_to'))
    except ObjectDoesNotExist:
        messages.error(request, "Account {} not found."
            .format(request.POST.get('account_to')))
        return
    if amount != Decimal(request.POST.get('confirm_amount')):
        messages.error(request, "You input two different amounts. Please try again.")
        error = True
    if not error:
        account_to.balance += amount
        account_to.save()
        new_transaction = History(
            account_number=account_to, 
            transaction_type="D",
            amount=amount,
            description="-",
        )
        new_transaction.save()
        messages.success(request, "Successfully deposited ${} to account number {}."
            .format(amount, mask_account_number(account_to.account_number))) 


def withdraw(request):
    amount = Decimal(request.POST.get('amount'))
    error = False

    try:
        account_from = Account.objects.get(account_number=request.POST.get('account_from'))
    except ObjectDoesNotExist:
        messages.error(request, "Account {} not found."
            .format(request.POST.get('account_from')))
        return
    if account_from.balance < amount:
        messages.error(request, "Your balance is too low.")
        error = True
    if account_from.user_id != request.user:
        messages.error(request, "You don't own that account.")
        error = True
    if amount != Decimal(request.POST.get('confirm_amount')):
        messages.error(request, "You input two different amounts. Please try again.")
        error = True
    if not error:
        account_from.balance -= amount
        account_from.save()
        new_transaction = History(
            account_number=account_from, 
            transaction_type="W",
            amount=amount*-1,
            description="-",
        )
        new_transaction.save()
        messages.success(request, 'Successfully withdrew ${} from account {}.'
            .format(amount, mask_account_number(account_from.account_number)))


def generate_account_number(user):
    account_number = ""
    for _ in range(16):
        account_number += str(random.randint(0,9))
    account_number = int(account_number)
    if not Account.objects.filter(account_number=account_number):
        new_account = Account(account_number=account_number, user_id=user, balance=0.00)
        new_account.save()
    else:
        generate_account_number(user)


def mask_account_number(account_number):
    return str(account_number)[0:4] + " **** **** " + str(account_number)[12:]