"""
Views for user authentication using JWT tokens.

This module provides:
- RegistrationView: Create new user accounts.
- LoginView: Authenticate a user and set JWT cookies.
- LogoutView: Blacklist refresh tokens and remove cookies.
- RefreshTokenView: Issue new access tokens using the refresh token stored in cookies.
"""

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken, TokenError

from .serializers import RegistrationSerializer, LoginSerializer


class RegistrationView(APIView):
    """
    Handle user registration.

    Accepts:
    - username, email, password, confirmed_password

    Returns:
    - 201 Created on successful signup
    - 400 Bad Request on validation errors
    """

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"detail": "User created successfully!"},
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class LoginView(TokenObtainPairView):
    """
    Handle user login using JWT authentication.

    Extends TokenObtainPairView:
    - Sets access & refresh tokens as HttpOnly cookies.
    - Returns basic user information.
    """

    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        refresh = response.data.get("refresh")
        access = response.data.get("access")
        user_data = response.data.get("user")

        # Store tokens in HttpOnly cookies
        response.set_cookie(
            key="access_token",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        response.set_cookie(
            key="refresh_token",
            value=refresh,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        # Clean response body
        response.data = {
            "detail": "Login successfully!",
            "user": user_data,
        }

        return response


class LogoutView(APIView):
    """
    Handle user logout.

    - Reads refresh token from cookies.
    - Attempts to blacklist it.
    - Deletes both access and refresh cookies.
    """

    def post(self, request, *args, **kwargs):
        refresh_cookie = request.COOKIES.get("refresh_token")

        if refresh_cookie:
            try:
                token = RefreshToken(refresh_cookie)
                token.blacklist()
            except TokenError:
                # Token is already invalid or cannot be blacklisted
                pass

        response = Response(
            {
                "detail": (
                    "Log-Out successfully! All tokens deleted. "
                    "Refresh token is now invalid."
                )
            },
            status=status.HTTP_200_OK,
        )

        # Remove cookies
        response.delete_cookie("access_token", path="/")
        response.delete_cookie("refresh_token", path="/")

        return response


class RefreshTokenView(TokenRefreshView):
    """
    Issue a new access token using the refresh token stored in cookies.

    Returns:
    - 200 OK with new access token
    - 401 Unauthorized if refresh token missing or invalid
    """

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")

        if refresh_token is None:
            return Response(
                {"detail": "Refresh token not provided."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        serializer = self.get_serializer(data={"refresh": refresh_token})

        try:
            serializer.is_valid(raise_exception=True)
        except Exception:
            return Response(
                {"detail": "Invalid refresh token."},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        access_token = serializer.validated_data.get("access")

        response = Response(
            {
                "detail": "Token refreshed",
                "access": access_token,
            },
            status=status.HTTP_200_OK,
        )

        # Update access token cookie
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="Lax",
        )

        return response
