from django.contrib.auth.models import User

from .models import Account, History


def transfer(amount, user, account_number_from, routing_number_to):
    account_from = Account.objects.filter(account_number=account_number_from)
    account_to = Account.object.filter(routing_number=routing_number_to)

    if amount is None:
        print("transfer: amount is None")
    elif account_from.balance < amount:
        print('transfer: account has too low balance')
    elif account_from is None:
        print('transfer: account_from not found')
    elif account_to is None:
        print('transfer: account_to not found')
    elif account_from.user_id is not user.id:
        print('transfer: you don\'t own that account')
    else:
        account_from.balance -= amount
        account_to.balance += amount
        account_from.save()
        account_to.save()
        log_transaction()


def deposit(amount, user, routing_number_to):
    account_to = Account.object.filter(routing_number=routing_number_to)

    if amount is None:
        print("deposit: amount is None")
    elif account_to is None:
        print('deposit: account_to not found')
    else:
        account_to += amount
        account_to.save()
        log_transaction() 


def withdraw(amount, user, account_number_from):
    account_from = Account.objects.filter(account_number=account_number_from)

    if amount is None:
        print("withdraw: amount is None")
    elif account_from.balance < amount:
        print('withdraw: account has too low balance')
    elif account_from is None:
        print('withdraw: account_from not found')
    elif account_from.user_id is not user.id:
        print('withdraw: you don\'t own that account')
    else:
        account_from.balance -= amount
        account_from.save()
        log_transaction()


def log_transaction():
    return