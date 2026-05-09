"""
config/wsgi.py

WSGI application entry point for the LGB Platform.
Used by production WSGI servers (gunicorn, uWSGI).
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    "config.settings.dev",
)

application = get_wsgi_application()
