from django.db import models

# Create your models here.

from django.db import models
from django.contrib.auth.models import User
import random

from django.db import models
from django.contrib.auth.models import User
import random

class Account(models.Model):
    ACCOUNT_TYPES = [
        ('saving', 'Saving Account'),
        ('current', 'Current Account'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accounts')
    account_number = models.CharField(max_length=10, unique=True, blank=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES)
    phone_number = models.IntegerField()
    email = models.EmailField()
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.account_number:
            self.account_number = self.generate_account_number()
        super().save(*args, **kwargs)

    @staticmethod
    def generate_account_number():
        """Generate a 10-digit unique account number."""
        while True:
            account_number = ''.join([str(random.randint(0, 9)) for _ in range(10)])
            if not Account.objects.filter(account_number=account_number).exists():
                return account_number

    def __str__(self):
        return f"{self.get_account_type_display()} ({self.account_number}) for {self.user.username}"

class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=10, choices=(('deposit', 'Deposit'), ('withdraw', 'Withdraw')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.transaction_type.capitalize()} of ${self.amount} on {self.timestamp}"
