from celery import shared_task
from django.db import transaction
from order_service.celery import app
from utils import external_exchange_utils
from .models import Order, Token
from sentry_sdk import capture_exception


'''
 solution 1 ) using app.task and gWorkers to run them asynchronously as soon as an order request received.
 with this solution we don't need any schedulers and therefor if we have free workers and resources,
 we will have far better performance compared to scheduled based routines.
'''
@app.task(name="aggregate_buy_orders_from_exchange")
def aggregate_buy_orders_from_exchange(symbol, minimum_value):
    token = Token.objects.get(symbol=symbol)

    with transaction.atomic():
        # token = Token.objects.filter(symbol=symbol).first()
        orders = Order.objects.select_for_update().filter(token=token, is_aggregated=False)

        # satisfying minimum order price condition
        total_value = sum(orders.values_list('price_value', flat=True))

        # amount to buy in total from the external exchange
        total_amount = sum(orders.values_list('amount', flat=True))

        if total_value > minimum_value:
            try:
                external_exchange_utils.buy_from_exchange(token.symbol, total_amount, token.price_unit)
                orders.update(is_aggregated=True)
            except Exception as e:
                #exception handling logic
                capture_exception(e)
                raise e

'''
 solution 2 ) using a shared_task with celery beat, looping through the orders per token
 this solution is not performant! so I don't use it
'''
# @shared_task
# def aggregate_all_orders_per_token(minimum_value):
#     tokens_list = Token.objects.all()
#     for token in tokens_list:
#         orders = Order.objects.filter(token=token, is_aggregated=False)
#         total_value = sum(orders.values_list('price_value', flat=True))
#
#         if total_value < minimum_value:
#             continue
#
#         total_amount = sum(orders.values_list('amount', flat=True))
#         try:
#             external_exchange_utils.buy_from_exchange(token.symbol, total_amount, token.price_unit)
#             orders.update(is_aggregated=True)
#         except Exception as e:
#             # exception handling logic
#             capture_exception(e)
#             raise e

'''
 solution 3 ) for each token, we hard code a separate tasks like this and use celery beat.
 with this approach we could use different queues to improve the performance
 but if we have 100 tokens listed on our exchange, then we will have to write down and hard code 100 different tasks here.
'''
# @shared_task(name='aggregate_orders_for_aban', queue='ABAN')
# def aggregate_orders_for_aban(minimum_value):
#     token = Token.objects.filter(symbol='ABAN').first()
#     orders = Order.objects.select_for_update().filter(token=token, is_aggregated=False)
#
#     # satisfying minimum order price condition
#     total_value = sum(orders.values_list('price_value', flat=True))
#     # amount to buy in total from the external exchange
#     total_amount = sum(orders.values_list('amount', flat=True))
#
#     # release the lock and return
#     if total_value < minimum_value:
#         try:
#             external_exchange_utils.buy_from_exchange(token.symbol, total_amount, token.price_unit)
#             orders.update(is_aggregated=True)
#         except Exception as e:
#             # exception handling logic
#             capture_exception(e)
#             raise e
#
# @shared_task(name='aggregate_orders_for_erc20', queue='ERC20')
# def aggregate_orders_for_erc20(minimum_value):
#     token = Token.objects.filter(symbol='ERC20').first()
#     orders = Order.objects.select_for_update().filter(token=token, is_aggregated=False)
#
#     # satisfying minimum order price condition
#     total_value = sum(orders.values_list('price_value', flat=True))
#     # amount to buy in total from the external exchange
#     total_amount = sum(orders.values_list('amount', flat=True))
#
#     # release the lock and return
#     if total_value < minimum_value:
#         try:
#             external_exchange_utils.buy_from_exchange(token.symbol, total_amount, token.price_unit)
#             orders.update(is_aggregated=True)
#         except Exception as e:
#             # exception handling logic
#             capture_exception(e)
#             raise e