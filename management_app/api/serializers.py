import re
from rest_framework import serializers
from urllib.parse import urlparse, parse_qs
from management_app.models import Question, Quiz
from management_app.services.quiz_pipeline_stub import build_quiz_stub
from management_app.services.persist_quiz import persist_quiz
from management_app.services.error import AIPipelineError

YOUTUBE_DOMAINS = {"youtube.com", "www.youtube.com", "m.youtube.com", "youtu.be"}
VIDEO_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")

class QuestionSerializer(serializers.ModelSerializer):
    question_options = serializers.ListField(
        child=serializers.CharField(),
        min_length=4,
        max_length=4
    )

    class Meta:
        model = Question
        fields = ['id', 'question_title', 'question_options',
                  'answer', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)

    class Meta:
        model = Quiz
        fields = ['id', 'title', 'description', 'created_at', 'updated_at',
                  'video_url', 'questions']
        read_only_fields = ['id', 'created_at', 'updated_at']

class CreateQuizSerializer(serializers.Serializer):
    url = serializers.URLField()

    def validate_url(self, value):
        parsed = urlparse(value.strip())
        netloc = parsed.netloc.lower()

        if netloc not in YOUTUBE_DOMAINS:
            raise serializers.ValidationError("URL must be a YouTube link.")

        video_id = None
        if netloc in {"youtube.com", "www.youtube.com", "m.youtube.com"}:
            video_id = parse_qs(parsed.query).get("v", [None])[0]
        elif netloc == "youtu.be":
            video_id = parsed.path.lstrip("/")

        if not video_id or not VIDEO_ID_RE.match(video_id):
            raise serializers.ValidationError("Invalid YouTube video ID.")

        return f"https://www.youtube.com/watch?v={video_id}"
    
    def create(self, validated_data):
        user = self.context["request"].user
        video_url = validated_data["url"]

        try:
            payload = build_quiz_stub(video_url)
        except AIPipelineError:
            raise

        quiz = persist_quiz(owner=user, video_url=video_url, payload=payload)

        return quiz
        
