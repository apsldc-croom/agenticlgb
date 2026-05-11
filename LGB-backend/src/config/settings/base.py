"""
config/settings/base.py

Base Django settings for the LGB Platform.
------------------------------------------
Common settings shared across all environments.
Environment-specific overrides live in dev.py, staging.py, production.py.

Settings are loaded via django-environ for 12-factor compliance.
"""

from datetime import timedelta
from pathlib import Path

import environ

# ---------------------------------------------------------
# PATHS
# ---------------------------------------------------------
# BASE_DIR = LGB-backend/src/
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# Root of the repository (LGB-backend/)
ROOT_DIR = BASE_DIR.parent

# ---------------------------------------------------------
# ENVIRONMENT
# ---------------------------------------------------------
env = environ.Env(
    DEBUG=(bool, False),
    ALLOWED_HOSTS=(list, ["localhost", "127.0.0.1"]),
)

# Read .env files — walk up to repo root for shared env
_env_file = ROOT_DIR.parent / ".env.dev"
if _env_file.exists():
    env.read_env(str(_env_file))

# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------
SECRET_KEY = env(
    "DJANGO_SECRET_KEY",
    default="django-insecure-lgb-dev-change-in-production!",
)

DEBUG = env("DEBUG", default=False)

ALLOWED_HOSTS = env("ALLOWED_HOSTS", default=["localhost", "127.0.0.1"])

# ---------------------------------------------------------
# APPLICATION REGISTRY
# ---------------------------------------------------------
DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    "django_filters",
]

LOCAL_APPS = [
    "core.users.apps.UsersConfig",
    "pm.apps.PmConfig",
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ---------------------------------------------------------
# URL CONFIGURATION
# ---------------------------------------------------------
ROOT_URLCONF = "config.urls"

WSGI_APPLICATION = "config.wsgi.application"

ASGI_APPLICATION = "config.asgi.application"

# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            BASE_DIR / "templates",
        ],
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

# ---------------------------------------------------------
# DATABASE
# ---------------------------------------------------------
DATABASES = {
    "default": env.db(
        "DATABASE_URL",
        default="sqlite:///db.sqlite3",
    ),
}

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# ---------------------------------------------------------
# AUTH
# ---------------------------------------------------------
AUTH_USER_MODEL = "users.User"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

# ---------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------
LANGUAGE_CODE = "en-us"

TIME_ZONE = "Asia/Kolkata"

USE_I18N = True

USE_TZ = True

# ---------------------------------------------------------
# STATIC & MEDIA
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = ROOT_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = ROOT_DIR / "media"

# ---------------------------------------------------------
# REST FRAMEWORK
# ---------------------------------------------------------
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 20,
    "DEFAULT_RENDERER_CLASSES": [
        "rest_framework.renderers.JSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
}

# ---------------------------------------------------------
# SIMPLE JWT
# ---------------------------------------------------------
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(minutes=30),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "ROTATE_REFRESH_TOKENS": True,
    "BLACKLIST_AFTER_ROTATION": True,
    "AUTH_HEADER_TYPES": ("Bearer",),
    # Use enriched serializer that returns user profile alongside tokens
    "TOKEN_OBTAIN_SERIALIZER": "core.users.serializers.LGBTokenObtainPairSerializer",
}

# ---------------------------------------------------------
# CORS
# ---------------------------------------------------------
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=[
        "http://localhost:3000",
        "http://localhost:5173",
    ],
)

CORS_ALLOW_CREDENTIALS = True

# ---------------------------------------------------------
# CELERY
# ---------------------------------------------------------
CELERY_BROKER_URL = env(
    "CELERY_BROKER_URL",
    default="redis://localhost:6379/0",
)

CELERY_RESULT_BACKEND = env(
    "CELERY_RESULT_BACKEND",
    default="redis://localhost:6379/1",
)

CELERY_ACCEPT_CONTENT = ["json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_TIMEZONE = TIME_ZONE

# ---------------------------------------------------------
# LOGGING
# ---------------------------------------------------------
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {
            "format": "[{asctime}] {levelname} {name} {message}",
            "style": "{",
        },
        "simple": {
            "format": "{levelname} {message}",
            "style": "{",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
        "pm": {
            "handlers": ["console"],
            "level": "DEBUG",
            "propagate": False,
        },
    },
}
