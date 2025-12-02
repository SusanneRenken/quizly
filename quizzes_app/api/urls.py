"""
URL configuration for quiz creation and quiz management endpoints.

Provides:
- POST /createQuiz/ → Generate a quiz from a YouTube URL.
- CRUD operations for quizzes via QuizViewSet (registered under /quizzes/).
"""

from django.urls import path, include
from rest_framework import routers
from .views import QuizCreateView, QuizViewSet

router = routers.SimpleRouter()
router.register(r"quizzes", QuizViewSet, basename="quiz")

urlpatterns = [
    path("createQuiz/", QuizCreateView.as_view(), name="create-quiz"),
    path("", include(router.urls)),
]
