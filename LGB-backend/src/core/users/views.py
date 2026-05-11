"""
core/users/views.py

DRF Views for user management and auth profile.
"""

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .permissions import IsAdminRole, IsPMOrAbove
from .serializers import (
    LGBTokenObtainPairSerializer,
    UserCreateSerializer,
    UserSerializer,
)


# =========================================================
# JWT LOGIN — enriched response
# =========================================================

class LGBTokenObtainPairView(TokenObtainPairView):
    """
    POST /api/v1/auth/token/
    Returns access + refresh tokens AND user profile.
    Replaces the default SimpleJWT view.
    """
    serializer_class = LGBTokenObtainPairSerializer


# =========================================================
# CURRENT USER
# =========================================================

class MeView(APIView):
    """
    GET /api/v1/auth/me/
    Returns the currently authenticated user's profile.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def patch(self, request):
        """Allow users to update their own full_name."""
        serializer = UserSerializer(
            request.user,
            data=request.data,
            partial=True,
        )
        serializer.is_valid(raise_exception=True)
        # Only allow updating safe fields
        allowed = {"full_name"}
        for key in list(serializer.validated_data.keys()):
            if key not in allowed:
                serializer.validated_data.pop(key)
        serializer.save()
        return Response(serializer.data)


# =========================================================
# USER MANAGEMENT (Admin only)
# =========================================================

class UserListCreateView(generics.ListCreateAPIView):
    """
    GET  /api/v1/users/       — list all users (PM+)
    POST /api/v1/users/       — create user (Admin only)
    """
    queryset = User.objects.all().order_by("full_name")

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAdminRole()]
        return [IsPMOrAbove()]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return UserCreateSerializer
        return UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET    /api/v1/users/{id}/  — get user (PM+)
    PATCH  /api/v1/users/{id}/  — update user role/status (Admin only)
    DELETE /api/v1/users/{id}/  — delete user (Admin only)
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.request.method in ("PATCH", "PUT", "DELETE"):
            return [IsAdminRole()]
        return [IsPMOrAbove()]
