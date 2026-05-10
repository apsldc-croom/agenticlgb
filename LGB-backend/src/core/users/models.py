"""
core/users/models.py

Custom User model for the LGB Platform.
----------------------------------------
- Email-based authentication (no username)
- RBAC roles: admin, pm, developer, viewer, agent
- AbstractBaseUser + PermissionsMixin for full Django auth
"""

from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models


# =========================================================
# ROLE CHOICES
# =========================================================

ROLE_CHOICES = [
    ("admin", "Admin"),           # Full access — system administrator
    ("pm", "Project Manager"),    # Manage projects, tasks, milestones
    ("developer", "Developer"),   # View + update own tasks
    ("viewer", "Viewer"),         # Read-only across all PM data
    ("agent", "Agent/System"),    # API-only role for AI/automation agents
]


# =========================================================
# USER MANAGER
# =========================================================

class UserManager(BaseUserManager):
    """
    Custom manager for email-based authentication.
    Replaces Django's default username-based manager.
    """

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Email address is required.")

        email = self.normalize_email(email)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "developer")

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")

        if not extra_fields.get("is_staff"):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get("is_superuser"):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


# =========================================================
# USER MODEL
# =========================================================

class User(AbstractBaseUser, PermissionsMixin):
    """
    LGB Platform User.

    Authentication:
    - Login via email + password
    - JWT tokens (SimpleJWT configured in settings)

    RBAC:
    - role field drives permission checks
    - Django groups/permissions also available via PermissionsMixin

    Fields:
    - email          → unique login identifier
    - full_name      → display name
    - role           → RBAC role (admin/pm/developer/viewer/agent)
    - is_active      → account enabled
    - is_staff       → Django admin access
    - date_joined    → audit timestamp
    """

    email = models.EmailField(
        unique=True,
        verbose_name="Email Address",
    )

    full_name = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Full Name",
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default="developer",
        verbose_name="Role",
        db_index=True,
    )

    is_active = models.BooleanField(
        default=True,
        verbose_name="Active",
    )

    is_staff = models.BooleanField(
        default=False,
        verbose_name="Staff (Admin site access)",
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Date Joined",
    )

    # Replace default manager
    objects = UserManager()

    # Use email instead of username for authentication
    USERNAME_FIELD = "email"

    # Required fields for createsuperuser (besides email + password)
    REQUIRED_FIELDS = ["full_name"]

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"
        ordering = ["full_name", "email"]

    def __str__(self):
        return f"{self.full_name} <{self.email}>"

    def get_full_name(self):
        return self.full_name or self.email

    def get_short_name(self):
        return self.full_name.split()[0] if self.full_name else self.email

    # ----------------------------------------------------------
    # RBAC convenience properties
    # ----------------------------------------------------------

    @property
    def is_admin(self):
        return self.role == "admin" or self.is_superuser

    @property
    def is_pm(self):
        return self.role in ("admin", "pm") or self.is_superuser

    @property
    def is_developer(self):
        return self.role in ("admin", "pm", "developer") or self.is_superuser

    @property
    def is_viewer(self):
        return True  # All authenticated users can view

    @property
    def is_agent(self):
        return self.role == "agent"
