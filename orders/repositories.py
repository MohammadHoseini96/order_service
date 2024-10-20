from django.contrib.auth.models import User
from .models import Order, Token, Outbox, Wallet


class UserRepository:

    def get_user_by_id(self, user_id):
        return User.objects.get(id=user_id)

    def get_updatable_user_by_id(self, user_id):
        return User.objects.select_for_update().filter(id=user_id)

    def create_simple_user(self, username, password):
        return User.objects.create(username=username, password=password)

class WalletRepository:

    def get_wallet_by_id(self, wallet_id):
        return Wallet.objects.get(id=wallet_id)

    def get_wallet_by_user(self, user):
        return Wallet.objects.get(user=user)

    def get_updatable_wallet_by_user(self, user):
        return Wallet.objects.select_for_update().filter(user=user)

    def create(self, user, balance):
        return Wallet.objects.create(user=user, balance=balance)

class TokenRepository:

    def get_token_by_symbol(self, symbol):
        return Token.objects.get(symbol=symbol)

    def create(self, symbol, name, price_unit):
        return Token.objects.create(symbol=symbol, name=name, price_unit=price_unit)

class OrderRepository:

    def get_order_by_id(self, order_id):
        return Order.objects.get(id=order_id)

    def create(self, user, token, amount, value):
        return Order.objects.create(user=user, token=token, amount=amount, price_value=value)

    def get_not_aggregated_orders(self):
        return Order.objects.filter(is_aggregated=False)

class OutboxRepository:

    def get_outbox_by_id(self, outbox_id):
        return Outbox.objects.get(id=outbox_id)

    def create(self, user, order, amount, event_name):
        return Outbox.objects.create(user=user, order=order, amount=amount, event_name=event_name)
