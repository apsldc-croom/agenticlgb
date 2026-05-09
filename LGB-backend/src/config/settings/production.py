"""
config/settings/production.py

Production environment settings.
All secrets must come from environment variables or a vault.
"""

from .base import *  # noqa: F401, F403

# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------
DEBUG = False

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")  # noqa: F405

SECRET_KEY = env("DJANGO_SECRET_KEY")  # noqa: F405 — MUST be set in production

# ---------------------------------------------------------
# DATABASE — PostgreSQL
# ---------------------------------------------------------
DATABASES = {
    "default": env.db("DATABASE_URL"),  # noqa: F405
}

# ---------------------------------------------------------
# SECURITY HEADERS
# ---------------------------------------------------------
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31_536_000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ---------------------------------------------------------
# STATIC FILES — WhiteNoise or S3
# ---------------------------------------------------------
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.ManifestStaticFilesStorage"

# ---------------------------------------------------------
# EMAIL — Production SMTP
# ---------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST")  # noqa: F405
EMAIL_PORT = env.int("EMAIL_PORT", default=587)  # noqa: F405
EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")  # noqa: F405
EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
EMAIL_USE_TLS = True

# ---------------------------------------------------------
# LOGGING — JSON structured for production
# ---------------------------------------------------------
LOGGING["formatters"]["json"] = {  # noqa: F405
    "()": "django.utils.log.ServerFormatter",
    "format": "[{server_time}] {message}",
    "style": "{",
}

# ---------------------------------------------------------
# REST FRAMEWORK — No browsable API in production
# ---------------------------------------------------------
REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] = [  # noqa: F405
    "rest_framework.renderers.JSONRenderer",
]
