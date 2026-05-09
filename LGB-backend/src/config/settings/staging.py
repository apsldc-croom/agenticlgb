"""
config/settings/staging.py

Staging environment settings.
Mirrors production but with looser restrictions for QA.
"""

from .base import *  # noqa: F401, F403

# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------
DEBUG = False

ALLOWED_HOSTS = env.list(  # noqa: F405
    "ALLOWED_HOSTS",
    default=["staging.lgb.example.com"],
)

# ---------------------------------------------------------
# DATABASE — PostgreSQL on staging
# ---------------------------------------------------------
DATABASES = {
    "default": env.db(  # noqa: F405
        "DATABASE_URL",
        default="postgres://lgb:lgb@localhost:5432/lgb_staging",
    ),
}

# ---------------------------------------------------------
# SECURITY HEADERS
# ---------------------------------------------------------
SECURE_SSL_REDIRECT = False  # Handled by nginx/LB
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# ---------------------------------------------------------
# EMAIL — SMTP on staging
# ---------------------------------------------------------
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = env("EMAIL_HOST", default="smtp.example.com")  # noqa: F405
EMAIL_PORT = env.int("EMAIL_PORT", default=587)  # noqa: F405
EMAIL_USE_TLS = True
