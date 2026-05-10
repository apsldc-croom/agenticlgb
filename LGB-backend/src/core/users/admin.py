"""
core/users/admin.py

Django Admin configuration for the User model.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    """
    Custom admin for the email-based User model.
    Replaces 'username' references with 'email'.
    """

    model = User
    list_display = [
        "email",
        "full_name",
        "role",
        "is_active",
        "is_staff",
        "date_joined",
    ]
    list_filter = [
        "role",
        "is_active",
        "is_staff",
        "is_superuser",
    ]
    search_fields = ["email", "full_name"]
    ordering = ["full_name", "email"]
    readonly_fields = ["date_joined", "last_login"]

    # Fieldsets for the detail/edit view
    fieldsets = (
        (None, {
            "fields": ("email", "password"),
        }),
        (_("Personal Info"), {
            "fields": ("full_name",),
        }),
        (_("Role & Permissions"), {
            "fields": (
                "role",
                "is_active",
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            ),
        }),
        (_("Timestamps"), {
            "fields": ("date_joined", "last_login"),
        }),
    )

    # Fieldsets for the create (add) view
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "full_name",
                "role",
                "password1",
                "password2",
                "is_active",
                "is_staff",
            ),
        }),
    )
