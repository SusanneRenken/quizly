"""
URL configuration for authentication endpoints.

This module defines the URL routes for user registration, login,
logout, and token refresh using JWT-based authentication.
"""

from django.urls import path
from .views import RegistrationView, LoginView, LogoutView, RefreshTokenView

urlpatterns = [
    path("register/", RegistrationView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("token/refresh/", RefreshTokenView.as_view(), name="token_refresh"),
]