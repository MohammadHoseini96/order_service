from orders.tasks import aggregate_buy_orders_from_exchange
from django.conf import settings
from django.db import transaction
from orders.repositories import UserRepository, TokenRepository, OrderRepository, OutboxRepository
from utils import external_exchange_utils


class PurchaseService:
    def __init__(
            self,
            user_service: UserRepository,
            token_repo: TokenRepository,
            order_repo: OrderRepository,
            outbox_repo: OutboxRepository,
    ):
        self.user_service = user_service
        self.token_repo = token_repo
        self.order_repo = order_repo
        self.outbox_repo = outbox_repo

    def deduce_token_price_value_from_user_balance(self, user, symbol, amount):
        print(user.username, symbol, amount)
        token = self.token_repo.get_token_by_symbol(symbol)
        price_value = external_exchange_utils.get_price(symbol, token.price_unit) * amount

        with transaction.atomic():
            user = self.user_service.get_updatable_user_by_id(user.id)
            if user.wallet.balance < price_value:
                raise Exception('not enough balance!')

            user.wallet.balance -= price_value
            user.wallet.save()

        order = self.order_repo.create(user, token, amount, price_value)
        self.outbox_repo.create(user, order, amount, "DEDUCED")

        return order