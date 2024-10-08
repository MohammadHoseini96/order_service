from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.response import Response
from .services import PurchaseService
from .repositories import UserRepository, TokenRepository, OrderRepository, OutboxRepository
from .serializers import OrderSerializer
from decimal import Decimal
from orders.tasks import aggregate_buy_orders_from_exchange
from django.conf import settings

# Create your views here.

userRepo = UserRepository()
tokenRepo = TokenRepository()
orderRepo = OrderRepository()
outboxRepo = OutboxRepository()

purchaseService = PurchaseService(userRepo, tokenRepo, orderRepo, outboxRepo)


class OrdersViewSet(viewsets.ViewSet):
    def create(self, request):
        user = request.user
        symbol = request.data.get('symbol')
        amount = Decimal(request.data.get('amount'))

        try:
            order = purchaseService.deduce_token_price_value_from_user_balance(user, symbol, amount)

            # celery task to be processed asynchronously with gevent workers
            aggregate_buy_orders_from_exchange.delay(symbol, settings.ORDERS_AGGREGATE_THRESHOLD)

            # if directly called, it will be synchronous blocking
            # aggregate_buy_orders_from_exchange(order.token.symbol, settings.ORDERS_AGGREGATE_THRESHOLD)

            return Response(OrderSerializer(order).data)
        except Exception as e:
            return Response({'error': str(e)}, status=500)
