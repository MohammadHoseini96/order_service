import logging
from decouple import config  # NoQA
import sentry_sdk
from sentry_sdk.integrations.celery import CeleryIntegration
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration


sentry_sdk.init(
    dsn=config("SENTRY_DSN", ""),
    integrations=[
        DjangoIntegration(),
        RedisIntegration(),
        CeleryIntegration(),
        LoggingIntegration(level=logging.INFO, event_level=logging.WARNING),
    ],
    traces_sample_rate=1,
    send_default_pii=True,
)
