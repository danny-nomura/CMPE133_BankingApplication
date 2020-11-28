from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Account(models.Model):
    account_number  = models.IntegerField(primary_key=True)
    routing_number  = models.IntegerField(unique=True)
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    balance         = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return self.account_number


class History(models.Model):
    TRANSACTION_TYPES = (
        ('T', 'Transfer'),
        ('D', 'Deposit'),
        ('W', 'Withdraw'),
    )

    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    datetime        = models.DateTimeField(default=timezone.now)
    transaction_type= models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount          = models.DecimalField(max_digits=20, decimal_places=2)