"""
config/settings/dev.py

Development environment settings.
Inherits from base and enables debug tooling.
"""

from .base import *  # noqa: F401, F403

# ---------------------------------------------------------
# DEBUG MODE
# ---------------------------------------------------------
DEBUG = True

# ---------------------------------------------------------
# ALLOWED HOSTS — permissive for local dev
# ---------------------------------------------------------
ALLOWED_HOSTS = ["*"]

# ---------------------------------------------------------
# DEV-ONLY APPS
# ---------------------------------------------------------
INSTALLED_APPS += [  # noqa: F405
    "django_extensions",
]

try:
    import debug_toolbar  # noqa: F401

    INSTALLED_APPS += ["debug_toolbar"]
    MIDDLEWARE.insert(0, "debug_toolbar.middleware.DebugToolbarMiddleware")  # noqa: F405
    INTERNAL_IPS = ["127.0.0.1"]
except ImportError:
    pass

# ---------------------------------------------------------
# DATABASE
# Precedence:
#   1. DATABASE_URL env var (set by docker-compose)
#   2. Hardcoded localhost:5432 (direct host dev)
# ---------------------------------------------------------
import os as _os  # noqa: E402
if "DATABASE_URL" in _os.environ:
    DATABASES = {"default": env.db("DATABASE_URL")}  # noqa: F405
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": "postgres",
            "USER": "postgres",
            "PASSWORD": "123",
            "HOST": "localhost",
            "PORT": "5432",
            "OPTIONS": {"connect_timeout": 10},
        }
    }


# ---------------------------------------------------------
# EMAIL — Console backend for dev
# ---------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# ---------------------------------------------------------
# CORS — Allow all in dev
# ---------------------------------------------------------
CORS_ALLOW_ALL_ORIGINS = True

# ---------------------------------------------------------
# REST FRAMEWORK — Enable browsable API in dev
# ---------------------------------------------------------
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
    "rest_framework.renderers.BrowsableAPIRenderer",
]

# ---------------------------------------------------------
# LOGGING — Verbose in dev
# ---------------------------------------------------------
LOGGING["root"]["level"] = "DEBUG"  # noqa: F405
