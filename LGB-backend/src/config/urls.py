"""
config/urls.py

Root URL configuration for the LGB Platform.
"""

from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# ---------------------------------------------------------
# API v1 URL namespace
# ---------------------------------------------------------
api_v1_patterns = [
    # Auth — JWT
    path("auth/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Project Management
    path("pm/", include("pm.urls", namespace="pm")),
]

urlpatterns = [
    # Admin
    path("admin/", admin.site.urls),

    # API v1
    path("api/v1/", include((api_v1_patterns, "api-v1"))),
]

# Debug toolbar (dev only)
try:
    import debug_toolbar  # noqa: F401
    from django.conf import settings

    if settings.DEBUG:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
except ImportError:
    pass
