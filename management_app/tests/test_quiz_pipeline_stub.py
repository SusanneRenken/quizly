from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from management_app.models import Quiz


class CreateQuizStubTests(APITestCase):

    def setUp(self):
        # Testnutzer anlegen
        self.user = User.objects.create_user(
            username="tester", email="tester@example.com", password="secret123"
        )
        self.client.force_authenticate(user=self.user)  # JWT umgehen, direkt Auth

        self.url = reverse("create-quiz")

    def test_create_quiz_valid_url(self):
        """Ein gültiger YouTube-Link erzeugt ein Quiz mit 10 Fragen."""
        data = {"url": "https://www.youtube.com/watch?v=abcdefghijk"}
        res = self.client.post(self.url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)

        quiz = Quiz.objects.first()
        self.assertEqual(quiz.questions.count(), 10)
        self.assertIn("questions", res.data)
        self.assertEqual(len(res.data["questions"]), 10)

    def test_create_quiz_invalid_domain(self):
        """Ungültige Domain -> 400 Bad Request."""
        data = {"url": "https://example.com/video"}
        res = self.client.post(self.url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("URL must be a YouTube link.", str(res.data))

    def test_create_quiz_invalid_video_id(self):
        """Ungültige Video-ID -> 400 Bad Request."""
        data = {"url": "https://www.youtube.com/watch?v=123"}
        res = self.client.post(self.url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("Invalid YouTube video ID.", str(res.data))

    def test_requires_authentication(self):
        """Unauthenticated User -> 401 Unauthorized."""
        self.client.force_authenticate(user=None)
        data = {"url": "https://www.youtube.com/watch?v=abcdefghijk"}
        res = self.client.post(self.url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

class CreateQuizShortUrlTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="shorty", password="pw12345")
        self.client.force_authenticate(user=self.user)
        self.url = reverse("create-quiz")

    def test_create_quiz_with_youtu_be_url(self):
        """Teste youtu.be Kurz-URL (deckt elif-Zweig im Serializer)."""
        data = {"url": "https://youtu.be/abcdefghijk"}
        res = self.client.post(self.url, data, format="json")

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Quiz.objects.count(), 1)
        quiz = Quiz.objects.first()
        self.assertTrue(quiz.video_url.startswith("https://www.youtube.com/watch?v="))