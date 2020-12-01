from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Account(models.Model):
    account_number  = models.IntegerField(primary_key=True)
    user_id         = models.ForeignKey(User, on_delete=models.CASCADE)
    balance         = models.DecimalField(max_digits=20, decimal_places=2)

    def __str__(self):
        return str(self.account_number)
    
    class Meta:
        db_table='users_account'


class History(models.Model):
    TRANSACTION_TYPES = (
        ('T', 'Transfer'),
        ('D', 'Deposit'),
        ('W', 'Withdraw'),
    )

    account_number  = models.ForeignKey(Account, on_delete=models.CASCADE)
    datetime        = models.DateTimeField(default=timezone.now)
    transaction_type= models.CharField(max_length=1, choices=TRANSACTION_TYPES)
    amount          = models.DecimalField(max_digits=20, decimal_places=2)
    description     = models.CharField(max_length=256, default="empty")

    def __str__(self):
        return str(self.account_number)[0:4] + " **** **** " + str(self.account_number)[12:] + ": " + str(self.datetime) + ": $" + str(self.amount)
    class Meta:
        db_table='users_history'