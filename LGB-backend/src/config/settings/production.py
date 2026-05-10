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

import os as _os
_raw_hosts = _os.environ.get("ALLOWED_HOSTS", "34.93.126.189,localhost,127.0.0.1")
ALLOWED_HOSTS = [h.strip() for h in _raw_hosts.split(",") if h.strip()]

SECRET_KEY = env("DJANGO_SECRET_KEY")  # noqa: F405 — MUST be set in production

# ---------------------------------------------------------
# DATABASE — PostgreSQL
# ---------------------------------------------------------
DATABASES = {
    "default": env.db("DATABASE_URL"),  # noqa: F405
}

# ---------------------------------------------------------
# SECURITY HEADERS
# Set SECURE_SSL=true in .env.prod AFTER SSL certificate is installed
# ---------------------------------------------------------
_ssl = env.bool("SECURE_SSL", default=False)  # noqa: F405
SECURE_SSL_REDIRECT = _ssl
SECURE_HSTS_SECONDS = 31_536_000 if _ssl else 0
SECURE_HSTS_INCLUDE_SUBDOMAINS = _ssl
SECURE_HSTS_PRELOAD = _ssl
SESSION_COOKIE_SECURE = _ssl
CSRF_COOKIE_SECURE = _ssl
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Use regular StaticFilesStorage — nginx serves /static/ directly.
# Switch to ManifestStaticFilesStorage once collectstatic --post-process is
# part of the CI pipeline.
STATICFILES_STORAGE = "django.contrib.staticfiles.storage.StaticFilesStorage"

# ---------------------------------------------------------
# EMAIL — fallback to console if SMTP not configured yet
# ---------------------------------------------------------
_email_host = env("EMAIL_HOST", default="")  # noqa: F405
if _email_host:
    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_HOST = _email_host
    EMAIL_PORT = env.int("EMAIL_PORT", default=587)  # noqa: F405
    EMAIL_HOST_USER = env("EMAIL_HOST_USER", default="")  # noqa: F405
    EMAIL_HOST_PASSWORD = env("EMAIL_HOST_PASSWORD", default="")  # noqa: F405
    EMAIL_USE_TLS = True
else:
    EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

LOGGING.setdefault("formatters", {})["verbose"] = {  # noqa: F405
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
