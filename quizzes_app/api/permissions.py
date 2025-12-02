"""
Custom permission to ensure that only the quiz owner can access or modify a quiz.
"""

from rest_framework.permissions import BasePermission


class IsQuizOwner(BasePermission):
    """
    Permission class that grants access only if the requesting user
    is the owner of the quiz object.
    """

    def has_object_permission(self, request, view, obj):
        """
        Return True only if the quiz belongs to the authenticated user.
        """
        return obj.owner == request.user
