from django.contrib import admin
from django.http import JsonResponse
from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView, TokenVerifyView

from core.users.views import LGBTokenObtainPairView


# ---------------------------------------------------------
# Health Check
# ---------------------------------------------------------
def health_check(request):
    """
    GET /api/health/
    Used by CI/CD pipeline to confirm deploy success.
    """
    return JsonResponse({"status": "ok", "version": "0.1.0"})


# ---------------------------------------------------------
# API v1 URL namespace
# ---------------------------------------------------------
api_v1_patterns = [
    # Auth — JWT (enriched: returns user profile in login response)
    path("auth/token/", LGBTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/token/verify/", TokenVerifyView.as_view(), name="token_verify"),

    # Auth — Current user profile + user management
    path("auth/", include("core.users.urls", namespace="users")),

    # Project Management
    path("pm/", include("pm.urls", namespace="pm")),
]

urlpatterns = [
    # Health check (no auth required)
    path("api/health/", health_check, name="health-check"),

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
