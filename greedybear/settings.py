# This file is a part of GreedyBear https://github.com/honeynet/GreedyBear
# See the file 'LICENSE' for copying permission.
# flake8: noqa
import logging
import os

from django.core.management.utils import get_random_secret_key
from elasticsearch import Elasticsearch
from datetime import timedelta
from version import VERSION

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get("DJANGO_SECRET", None) or get_random_secret_key()

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.environ.get("DEBUG", False) == "True"

DJANGO_LOG_DIRECTORY = "/var/log/greedybear/django"
MOCK_CONNECTIONS = os.environ.get("MOCK_CONNECTIONS", False) == "True"
ELASTIC_ENDPOINT = os.getenv("ELASTIC_ENDPOINT", "").split(",")

SLACK_TOKEN = os.environ.get("SLACK_TOKEN", "")
SLACK_CHANNEL = os.environ.get("SLACK_CHANNEL", "")

ALLOWED_HOSTS = ["*"]

# Application definition
INSTALLED_APPS = [
    # default
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "django.contrib.postgres",
    "gui.apps.GuiConfig",
    # DRF
    "rest_framework",
    "durin",
    "drf_spectacular",
    # greedybear apps
    "api.apps.ApiConfig",
    "greedybear.apps.GreedyBearConfig",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "greedybear.urls"

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

WSGI_APPLICATION = "greedybear.wsgi.application"


REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
    ],
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "durin.auth.CachedTokenAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
    "EXCEPTION_HANDLER": "rest_framework.views.exception_handler",
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}

# DRF Spectacular
SPECTACULAR_SETTINGS = {
    "TITLE": "GreedyBear API specification",
    "VERSION": VERSION,
}

# Django-Rest-Durin
REST_DURIN = {
    "DEFAULT_TOKEN_TTL": timedelta(days=14),
    "TOKEN_CHARACTER_LENGTH": 32,
    "USER_SERIALIZER": "durin.serializers.UserSerializer",
    "AUTH_HEADER_PREFIX": "Token",
    "TOKEN_CACHE_TIMEOUT": 300,  # 5 minutes
    "REFRESH_TOKEN_ON_LOGIN": True,
}

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_NAME = os.environ.get("DB_NAME", "greedybear_db")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": DB_NAME,
        "HOST": DB_HOST,
        "PORT": DB_PORT,
        "USER": DB_USER,
        "PASSWORD": DB_PASSWORD,
    },
}

ELASTIC_CLIENT = Elasticsearch(
    ELASTIC_ENDPOINT,
    maxsize=20,
    retry_on_timeout=True,
    timeout=30,
)

BROKER_URL = os.environ.get("BROKER_URL", "amqp://guest:guest@rabbitmq:5672")
RESULT_BACKEND = "django-db"


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

USE_L10N = True

USE_TZ = False


# Static files (CSS, JavaScript, Images)

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "static/")


INFO_OR_DEBUG_LEVEL = "DEBUG" if DEBUG else "INFO"
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "stdfmt": {
            "format": "%(asctime)s - %(name)s - %(funcName)s - %(levelname)s - %(message)s",
        },
    },
    "handlers": {
        "celery": {
            "level": INFO_OR_DEBUG_LEVEL,
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/celery.log",
            "formatter": "stdfmt",
        },
        "celery_error": {
            "level": "ERROR",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/celery_errors.log",
            "formatter": "stdfmt",
        },
        "elasticsearch": {
            "level": INFO_OR_DEBUG_LEVEL,
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/elasticsearch.log",
            "formatter": "stdfmt",
        },
        "api": {
            "level": INFO_OR_DEBUG_LEVEL,
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/api.log",
            "formatter": "stdfmt",
        },
        "api_error": {
            "level": "ERROR",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/api_errors.log",
            "formatter": "stdfmt",
        },
        "gui": {
            "level": INFO_OR_DEBUG_LEVEL,
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/gui.log",
            "formatter": "stdfmt",
        },
        "gui_error": {
            "level": "ERROR",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/gui_errors.log",
            "formatter": "stdfmt",
        },
        "greedybear": {
            "level": INFO_OR_DEBUG_LEVEL,
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/greedybear.log",
            "formatter": "stdfmt",
        },
        "greedybear_error": {
            "level": "ERROR",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/greedybear_errors.log",
            "formatter": "stdfmt",
        },
        "django_unhandled_errors": {
            "level": "ERROR",
            "class": "logging.handlers.WatchedFileHandler",
            "filename": f"{DJANGO_LOG_DIRECTORY}/django_errors.log",
            "formatter": "stdfmt",
        },
    },
    "loggers": {
        "celery": {
            "handlers": ["celery", "celery_error"],
            "level": INFO_OR_DEBUG_LEVEL,
            "propagate": True,
        },
        "elasticsearch": {
            "handlers": ["elasticsearch"],
            "level": INFO_OR_DEBUG_LEVEL,
            "propagate": True,
        },
        "api": {
            "handlers": ["api", "api_error"],
            "level": INFO_OR_DEBUG_LEVEL,
            "propagate": True,
        },
        "gui": {
            "handlers": ["gui", "gui_error"],
            "level": INFO_OR_DEBUG_LEVEL,
            "propagate": True,
        },
        "greedybear": {
            "handlers": ["greedybear", "greedybear_error"],
            "level": INFO_OR_DEBUG_LEVEL,
            "propagate": True,
        },
        "django": {
            "handlers": ["django_unhandled_errors"],
            "level": "ERROR",
            "propagate": True,
        },
    },
}

# disable some really noisy logs
es_logger = logging.getLogger("elasticsearch")
if DEBUG:
    es_logger.setLevel(logging.INFO)
else:
    es_logger.setLevel(logging.WARNING)
