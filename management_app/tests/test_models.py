from django.test import TestCase
from django.contrib.auth.models import User
from management_app.models import Quiz, Question


class ModelStrTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="susanne", password="pw12345")
        self.quiz = Quiz.objects.create(
            owner=self.user,
            title="Testquiz",
            description="Beschreibung",
            video_url="https://youtu.be/abcdefghijk",
        )
        self.question = Question.objects.create(
            quiz=self.quiz,
            question_title="Was ist eine Stub-Pipeline?",
            question_options=["A", "B", "C", "D"],
            answer="A",
        )

    def test_quiz_str_returns_title_and_owner(self):
        """__str__ von Quiz soll Titel und Benutzername enthalten."""
        result = str(self.quiz)
        self.assertIn("Testquiz", result)
        self.assertIn("susanne", result)

    def test_question_str_returns_truncated_title(self):
        """__str__ von Question soll den Titel (max. 50 Zeichen) zurückgeben."""
        result = str(self.question)
        self.assertTrue(result.startswith("Was ist eine Stub-Pipeline"))
        self.assertLessEqual(len(result), 50)
