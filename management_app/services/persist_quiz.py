from django.db import transaction
from management_app.models import Quiz, Question

@transaction.atomic
def persist_quiz(*, owner, video_url: str, payload: dict) -> Quiz:
    quiz = Quiz.objects.create(
        owner=owner,
        video_url=video_url,
        title=payload["title"],
        description=payload.get("description", "")
    )
    Question.objects.bulk_create([
        Question(
            quiz=quiz,
            question_title=q["question_title"],
            question_options=q["question_options"],
            answer=q["answer"],
        )
        for q in payload["questions"]
    ])
    return quiz