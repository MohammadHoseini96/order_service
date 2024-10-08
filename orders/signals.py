from django.db.models.signals import pre_save

from orders.models import Order


def truncate_transaction_detail(sender, instance, **kwargs):
    """To truncate the `detail` field of transaction before saving"""
    if instance.error_detail is not None and len(instance.error_detail) > 64:
        instance.error_detail = f"{instance.error_detail[:60]}..."

pre_save.connect(truncate_transaction_detail, Order)
