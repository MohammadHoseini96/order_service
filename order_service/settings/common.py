from ast import literal_eval
from decimal import Decimal
from pathlib import Path

from decouple import config  # NoQA

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("SECRET_KEY")

DEBUG = config("DEBUG", False, cast=bool)

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # packages
    "rest_framework",
    "cachalot",
    # apps
    # "users",
    "orders",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "order_service.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "order_service.wsgi.application"


# Database

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": config("DEFAULT_DB_NAME"),
        "USER": config("DEFAULT_DB_USER"),
        "PASSWORD": config("DEFAULT_DB_PASSWORD"),
        "HOST": config("DEFAULT_DB_HOST", "localhost"),
        "PORT": config("DEFAULT_DB_PORT", ""),
    }
}


# Password validation

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)

STATIC_URL = "static/"
STATIC_ROOT = "./static/"

# Default primary key field type

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


# project specific settings

# ---------- USER MODEL ----------

# AUTH_USER_MODEL = "users.User"

# ---------- Rest Framework ----------

REST_FRAMEWORK = {
    "PAGE_SIZE": 50,
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "EXCEPTION_HANDLER": "utils.exception_handler.exception_handler",
}


# ---------- REDIS ----------

REDIS_HOST = config("REDIS_HOST", "localhost")
REDIS_PORT = config("REDIS_PORT", 6379)
REDIS_PASSWORD = config("REDIS_PASSWORD")
REDIS_USERNAME = config("REDIS_USERNAME")

REDIS_DJANGO_CACHE_DB = config("REDIS_DJANGO_CACHE_DB", "0")
REDIS_DJANGO_OM_DB = config("REDIS_DJANGO_OM_DB", "1")
REDIS_CELERY_DB = config("REDIS_CELERY_DB", "1")

REDIS_OM_URL = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DJANGO_OM_DB}"

# ---------- CELERY ----------
CELERY_BROKER_URL = f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_CELERY_DB}"
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_BEAT_SCHEDULE = {
    'check-and-combine-orders-every-minute': {
        'task': 'orders.tasks.check_and_combine_orders',
        'schedule': 60,
    },
}
CELERY_TIMEZONE = TIME_ZONE


# ---------- CACHALOT ----------

CACHALOT_ENABLED = True
# CACHALOT_TIMEOUT = 3_600 * 24
# CACHALOT_ONLY_CACHABLE_TABLES = frozenset(
#     (
#         "users_user",
#     )
# )


# ---------- CACHES ----------

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{REDIS_USERNAME}:{REDIS_PASSWORD}@{REDIS_HOST}:{REDIS_PORT}/{REDIS_DJANGO_CACHE_DB}",
        "OPTIONS": {"CLIENT_CLASS": "django_redis.client.DefaultClient"},
    }
}


# ---------- Others ----------

MAXIMUM_ACCEPT_REQUEST_TTL = 35  # time to receive requests from the services in seconds

ORDERS_AGGREGATE_THRESHOLD = Decimal(10)

REQUESTS_PROXY = literal_eval(config("REQUESTS_PROXY", "{}", cast=str))
