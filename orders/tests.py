import time

from django.test import TransactionTestCase
from django.contrib.auth.models import User
from .models import Wallet, Order
from .services import PurchaseService
from .repositories import UserRepository, WalletRepository, TokenRepository, OrderRepository, OutboxRepository
from decimal import Decimal
from orders.tasks import aggregate_buy_orders_from_exchange
from django.conf import settings

# Create your tests here.

class OrderTestCase(TransactionTestCase):
    def setUp(self):

        self.user_repo = UserRepository()
        self.wallet_repo = WalletRepository()
        self.token_repo = TokenRepository()
        self.order_repo = OrderRepository()
        self.outbox_repo = OutboxRepository()


        self.user = self.user_repo.create_simple_user(username='user', password='password')


        self.wallet_repo.create(user=self.user, balance=100)


        self.token = self.token_repo.create(symbol='ABAN', name='ABAN', price_unit='irToman')

        self.purchaseService = PurchaseService(
            self.user_repo,
            self.token_repo,
            self.order_repo,
            self.outbox_repo
        )

    def test_orders(self):
        # greater than 10$ limit if we assume the price is 4$ :
        order = self.purchaseService.deduce_token_price_value_from_user_balance(
            self.user,
            'ABAN',
            Decimal('3')
        )

        # celery task to be processed asynchronously with gevent workers
        aggregate_buy_orders_from_exchange.delay(order.token.symbol, settings.ORDERS_AGGREGATE_THRESHOLD)

        # if directly called, it will be synchronous blocking
        # aggregate_buy_orders_from_exchange(order.token.symbol, settings.ORDERS_AGGREGATE_THRESHOLD)

        time.sleep(1.5)
        self.assertEqual(order.price_value, 12)
        self.assertTrue(Order.objects.filter(id=order.id).exists())
        self.assertEqual(self.user.wallet.balance, 88)


        # smaller than 10$"
        order = self.purchaseService.deduce_token_price_value_from_user_balance(
            self.user,
            'ABAN',
            Decimal('1')
        )
        aggregate_buy_orders_from_exchange.delay(order.token.symbol, settings.ORDERS_AGGREGATE_THRESHOLD)

        order = self.purchaseService.deduce_token_price_value_from_user_balance(
            self.user,
            'ABAN',
            Decimal('1')
        )
        aggregate_buy_orders_from_exchange.delay(order.token.symbol, settings.ORDERS_AGGREGATE_THRESHOLD)

        order = self.purchaseService.deduce_token_price_value_from_user_balance(
            self.user,
            'ABAN',
            Decimal('1')
        )
        aggregate_buy_orders_from_exchange.delay(order.token.symbol, settings.ORDERS_AGGREGATE_THRESHOLD)
        time.sleep(2)
        self.assertEqual(order.price_value, 12)
        self.assertTrue(Order.objects.filter(id=order.id).exists())
        self.assertEqual(self.user.wallet.balance, 76)
