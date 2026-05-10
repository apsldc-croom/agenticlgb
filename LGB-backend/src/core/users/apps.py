"""
core/users/apps.py

Django app configuration for the Users module.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "core.users"
    label = "users"
    verbose_name = "Users & Auth"
