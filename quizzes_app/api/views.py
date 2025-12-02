"""
Views for quiz creation and quiz management.

This module provides:
- QuizCreateView: Generates a new quiz using the CreateQuizSerializer.
- QuizViewSet: Full CRUD operations for quizzes with owner-based permissions.
"""

from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from rest_framework.response import Response

from quizzes_app.models import Quiz
from quizzes_app.api.serializers import (
    QuizSerializer,
    CreateQuizSerializer,
    QuizWithTimestampsSerializer,
)
from quizzes_app.api.permissions import IsQuizOwner


class QuizCreateView(generics.CreateAPIView):
    """
    API endpoint for generating a new quiz.

    Uses:
    - CreateQuizSerializer for input validation & quiz generation.
    - Returns: QuizWithTimestampsSerializer containing created quiz data.
    """

    serializer_class = CreateQuizSerializer

    def create(self, request, *args, **kwargs):
        """
        Validate input, generate the quiz, and return the complete quiz data.
        """
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()

        return Response(
            QuizWithTimestampsSerializer(instance).data,
            status=status.HTTP_201_CREATED,
        )


class QuizViewSet(viewsets.ModelViewSet):
    """
    ViewSet for listing, retrieving, updating, and deleting quizzes.

    Permissions:
    - User must be authenticated.
    - Only the quiz owner can access or modify their quizzes.

    Behavior:
    - list: Only returns quizzes owned by the current user.
    - other actions (retrieve/update/delete): Allowed only for the quiz owner.
    """

    serializer_class = QuizSerializer
    permission_classes = [IsAuthenticated, IsQuizOwner]

    def get_queryset(self):
        """
        Restrict 'list' view to the user's quizzes.
        Allow full queryset for detail actions (permission controls access).
        """
        if self.action == "list":
            return Quiz.objects.filter(owner=self.request.user).order_by("-created_at")

        return Quiz.objects.all()
