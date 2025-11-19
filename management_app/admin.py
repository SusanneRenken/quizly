"""
Admin configuration for Quiz and Question models.

Provides:
- List display settings
- Search fields
- Filters
- Read-only fields
"""

from django.contrib import admin
from management_app.models import Quiz, Question


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Quiz model.

    Displays:
    - ID, title, owner, video URL, creation date

    Enables:
    - Searching by title, owner username, video URL
    - Filtering by creation date and owner
    """

    list_display = ("id", "title", "owner", "video_url", "created_at")
    search_fields = ("title", "owner__username", "video_url")
    list_filter = ("created_at", "owner")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model.

    Displays:
    - ID, quiz reference, question title, answer

    Enables:
    - Searching by question title, quiz title, answer
    - Filtering by quiz
    """

    list_display = ("id", "quiz", "question_title", "answer")
    search_fields = ("question_title", "quiz__title", "answer")
    list_filter = ("quiz",)
    readonly_fields = ("created_at", "updated_at")
