"""
Serializers for user registration and authentication.

This module contains:
- RegistrationSerializer: Handles user sign-up with password confirmation.
- LoginSerializer: Extends JWT TokenObtainPairSerializer to include user data in the response.
"""

from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegistrationSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    Validates:
    - Unique email.
    - Matching password and confirmed_password.

    Creates:
    - A new User instance with hashed password.
    """

    confirmed_password = serializers.CharField(write_only=True)
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirmed_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def validate(self, attrs):
        """
        Ensure that password and confirmed_password match.
        """
        if attrs["password"] != attrs["confirmed_password"]:
            raise serializers.ValidationError(
                {"confirmed_password": "Passwords do not match"}
            )
        return attrs

    def create(self, validated_data):
        """
        Create the user after removing confirmed_password from the payload.
        """
        validated_data.pop("confirmed_password")
        return User.objects.create_user(**validated_data)


class LoginSerializer(TokenObtainPairSerializer):
    """
    Serializer for user login with JWT.

    Extends:
    - Adds user info (id, username, email) to the token response.
    """

    def validate(self, attrs):
        """
        Validate login credentials and append user data to JWT response.
        """
        data = super().validate(attrs)

        user = getattr(self, "user", None)
        if user is not None:
            data["user"] = {
                "id": user.id,
                "username": user.username,
                "email": user.email,
            }

        return data
