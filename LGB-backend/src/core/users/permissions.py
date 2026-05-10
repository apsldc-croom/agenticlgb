"""
core/users/permissions.py

Custom DRF permission classes based on RBAC roles.
---------------------------------------------------
Usage:
    class MyView(APIView):
        permission_classes = [IsAuthenticated, IsPMOrAbove]
"""

from rest_framework.permissions import BasePermission


class IsAdminRole(BasePermission):
    """Only users with role='admin' or superusers."""

    message = "Admin role required."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsPMOrAbove(BasePermission):
    """Users with role='pm' or 'admin', or superusers."""

    message = "Project Manager role or above required."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_pm
        )


class IsDeveloperOrAbove(BasePermission):
    """Users with role='developer', 'pm', or 'admin'."""

    message = "Developer role or above required."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_developer
        )


class IsViewerOrAbove(BasePermission):
    """Any authenticated user (viewer and above)."""

    message = "Authentication required."

    def has_permission(self, request, view):
        return request.user.is_authenticated


class IsAgentOrAdmin(BasePermission):
    """Agents (system/automation) or admins only."""

    message = "Agent or Admin role required."

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and (request.user.is_agent or request.user.is_admin)
        )


class IsReadOnlyOrPMAbove(BasePermission):
    """
    Read-only for authenticated users.
    Write operations require PM role or above.
    """

    SAFE_METHODS = ("GET", "HEAD", "OPTIONS")

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.method in self.SAFE_METHODS:
            return True
        return request.user.is_pm
