from django.contrib import admin
from management_app.models import Quiz, Question


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "video_url", "created_at")
    search_fields = ("title", "owner__username", "video_url")
    list_filter = ("created_at", "owner")
    readonly_fields = ("created_at", "updated_at")


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "quiz", "question_title", "answer")
    search_fields = ("question_title", "quiz__title", "answer")
    list_filter = ("quiz",)
    readonly_fields = ("created_at", "updated_at")