"""
Views for quiz creation and quiz management.

This module provides:
- QuizCreateView: Generates a new quiz using the CreateQuizSerializer.
- QuizViewSet: Full CRUD operations for quizzes with owner-based permissions.
"""

from rest_framework import status, generics, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.conf import settings

from quizzes_app.models import Quiz
from quizzes_app.api.serializers import (
    QuizSerializer,
    CreateQuizSerializer,
    QuizWithTimestampsSerializer,
)
from quizzes_app.api.permissions import IsQuizOwner
from quizzes_app.services.quiz_pipeline_prod import build_quiz_prod
from quizzes_app.services.quiz_pipeline_stub import build_quiz_stub
from quizzes_app.services.persist_quiz import persist_quiz
from quizzes_app.services.error import AIPipelineError


class QuizCreateView(generics.CreateAPIView):
    """
    API endpoint for generating a new quiz.

    Workflow:
    1. Validate the input (YouTube URL) using CreateQuizSerializer.
    2. Execute the AI pipeline (Whisper/Gemini or stub), depending on project settings.
    3. Persist the generated quiz and its questions via the service layer.
    4. Return the created quiz with timestamps using QuizWithTimestampsSerializer.
    """

    serializer_class = CreateQuizSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user
        video_url = serializer.validated_data["url"]

        try:
            mode = getattr(settings, "QUIZLY_PIPELINE_MODE", "stub")
            if mode == "prod":
                payload = build_quiz_prod(video_url)
            else:
                payload = build_quiz_stub(video_url)
        except AIPipelineError as e:
            raise e

        quiz = persist_quiz(owner=user, video_url=video_url, payload=payload)

        output_data = QuizWithTimestampsSerializer(quiz).data
        return Response(output_data, status=status.HTTP_201_CREATED)


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
            user = getattr(self.request, "user", None)
            if not (user and user.is_authenticated):
                # If the requester is anonymous, return an empty queryset
                return Quiz.objects.none()

            return Quiz.objects.filter(owner=user).order_by("-created_at")

        return Quiz.objects.all()
