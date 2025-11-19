"""
Serializers for quiz and question handling.

Includes:
- QuestionSerializer: Basic question serialization.
- QuestionWithTimestampsSerializer: Adds created/updated timestamps.
- QuizSerializer: Basic quiz serialization including questions.
- QuizWithTimestampsSerializer: Extended version with timestamps.
- CreateQuizSerializer: Validates YouTube URL and triggers quiz generation.
"""

import re
from django.conf import settings
from rest_framework import serializers
from urllib.parse import urlparse, parse_qs

from management_app.models import Question, Quiz
from management_app.services.quiz_pipeline_prod import build_quiz_prod
from management_app.services.quiz_pipeline_stub import build_quiz_stub
from management_app.services.persist_quiz import persist_quiz
from management_app.services.error import AIPipelineError


YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")


class QuestionSerializer(serializers.ModelSerializer):
    """
    Serializer for quiz questions.

    Ensures:
    - Exactly 4 answer options.
    """

    question_options = serializers.ListField(
        child=serializers.CharField(),
        min_length=4,
        max_length=4,
    )

    class Meta:
        model = Question
        fields = ["id", "question_title", "question_options", "answer"]
        read_only_fields = ["id"]


class QuestionWithTimestampsSerializer(QuestionSerializer):
    """
    Extended question serializer that includes timestamps.
    """

    class Meta(QuestionSerializer.Meta):
        fields = QuestionSerializer.Meta.fields + ["created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]


class QuizSerializer(serializers.ModelSerializer):
    """
    Serializer for the Quiz model with nested questions (read-only).
    """

    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = [
            "id",
            "title",
            "description",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
            "video_url",
            "questions",
            "description",
        ]


class QuizWithTimestampsSerializer(serializers.ModelSerializer):
    """
    Extended quiz serializer including timestamps inside nested questions.
    """

    questions = QuestionWithTimestampsSerializer(many=True, read_only=True)

    class Meta(QuizSerializer.Meta):
        pass


class CreateQuizSerializer(serializers.Serializer):
    """
    Serializer for creating a quiz from a YouTube URL.

    Responsibilities:
    - Validate URL and extract YouTube video ID.
    - Normalize to a canonical video URL.
    - Trigger pipeline (stub or prod).
    - Persist generated quiz.
    """

    url = serializers.URLField()

    def validate_url(self, value):
        """
        Validate that the URL is a valid YouTube link and extract the video ID.
        Returns a normalized YouTube URL.
        """
        parsed = urlparse(value.strip())
        netloc = parsed.netloc.lower()

        if netloc not in YOUTUBE_DOMAINS:
            raise serializers.ValidationError("URL must be a YouTube link.")

        # Extract video ID depending on domain format
        video_id = None
        if netloc in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif netloc == "youtu.be":
            video_id = parsed.path.lstrip("/")

        if not video_id or not VIDEO_ID_RE.match(video_id):
            raise serializers.ValidationError("Invalid YouTube video ID.")

        return f"https://www.youtube.com/watch?v={video_id}"

    def create(self, validated_data):
        """
        Create a quiz using either the stub or prod pipeline, depending on settings.
        """
        user = self.context["request"].user
        video_url = validated_data["url"]

        try:
            mode = getattr(settings, "QUIZLY_PIPELINE_MODE", "stub")
            if mode == "prod":
                payload = build_quiz_prod(video_url)
            else:
                payload = build_quiz_stub(video_url)
        except AIPipelineError:
            # Pipeline errors propagate as-is for clear API error handling
            raise

        quiz = persist_quiz(owner=user, video_url=video_url, payload=payload)
        return quiz
