from django.contrib import admin

from orders.models import Wallet, Token, Order, Outbox

# Register your models here.


admin.site.register(Wallet)
admin.site.register(Token)
admin.site.register(Order)
admin.site.register(Outbox)