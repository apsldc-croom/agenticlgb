"""
core/users/urls.py

URL routing for user management endpoints.
"""

from django.urls import path

from .views import MeView, UserDetailView, UserListCreateView

app_name = "users"

urlpatterns = [
    # Current user profile
    path("me/", MeView.as_view(), name="me"),

    # User management (admin)
    path("", UserListCreateView.as_view(), name="user-list"),
    path("<int:pk>/", UserDetailView.as_view(), name="user-detail"),
]
