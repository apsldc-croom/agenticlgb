"""
core/users/serializers.py

DRF Serializers for the User model.
"""

from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from .models import User


# =========================================================
# USER SERIALIZERS
# =========================================================

class UserMiniSerializer(serializers.ModelSerializer):
    """Minimal user representation — used as nested field in Task, etc."""

    class Meta:
        model = User
        fields = ["id", "email", "full_name", "role"]
        read_only_fields = fields


class UserSerializer(serializers.ModelSerializer):
    """Full user profile serializer (read-only for most fields)."""

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "full_name",
            "role",
            "is_active",
            "is_staff",
            "date_joined",
        ]
        read_only_fields = [
            "id",
            "is_staff",
            "date_joined",
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating new users (admin only)."""

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = [
            "email",
            "full_name",
            "role",
            "password",
            "is_active",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


# =========================================================
# JWT TOKEN — enriched with user data
# =========================================================

class LGBTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Extended JWT serializer.
    Adds user info to the token response so the frontend
    doesn't need a separate /me/ call after login.
    """

    def validate(self, attrs):
        data = super().validate(attrs)
        data["user"] = UserSerializer(self.user).data
        return data
