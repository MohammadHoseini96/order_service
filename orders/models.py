from django.db import models
from django.contrib.auth.models import User


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=12, decimal_places=4, default=0)

class Token(models.Model):
    symbol = models.CharField(max_length=15)
    name = models.CharField(max_length=100)
    price_unit = models.CharField(max_length=20) # usDollar, irToman, ...

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    token = models.ForeignKey(Token, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=4)
    price_value = models.DecimalField(
        max_digits=12,
        decimal_places=4
    ) # value = amount * price (in price_unit)
    is_aggregated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

class Outbox(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=4)
    event_name = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
