"""
Models for quizzes and quiz questions.

This module defines:
- Quiz: Represents a generated quiz linked to a YouTube video.
- Question: Represents a single question belonging to a quiz.
"""

from django.db import models
from django.contrib.auth.models import User


class Quiz(models.Model):
    """
    Represents a quiz generated from a YouTube video.

    Fields:
    - title: Title of the quiz.
    - description: Optional description.
    - video_url: URL of the source YouTube video.
    - owner: User who owns the quiz.
    - created_at: Timestamp when the quiz was created.
    - updated_at: Timestamp when the quiz was last updated.
    """

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    video_url = models.URLField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="quizzes")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a readable representation of the quiz."""
        return f"{self.title} ({self.owner.username})"


class Question(models.Model):
    """
    Represents a quiz question.

    Fields:
    - quiz: Foreign key linking to the related quiz.
    - question_title: The text/title of the question.
    - question_options: A list of answer options (JSON).
    - answer: The correct answer.
    - created_at: Timestamp when the question was created.
    - updated_at: Timestamp when the question was last updated.
    """

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    question_title = models.CharField(max_length=255)
    question_options = models.JSONField(default=list)
    answer = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        """Return a truncated version of the question title."""
        return self.question_title[:50]
