from __future__ import absolute_import, unicode_literals

from decouple import config  # NoQA

from order_service.sentry import sentry_sdk

if config("ENTRYPOINT", "django") in ["celery"]:
    from .celery import app as celery_app  # NoQA

    __all__ = ("celery_app", "sentry_sdk")
else:
    __all__ = ("sentry_sdk",)
