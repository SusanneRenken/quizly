# management_app/tests/test_quiz_viewset.py

from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from management_app.models import Quiz, Question


class QuizViewSetTests(APITestCase):
    def setUp(self):
        self.client = APIClient()

        self.user1 = User.objects.create_user(
            username="user1", email="user1@example.com", password="password123"
        )
        self.user2 = User.objects.create_user(
            username="user2", email="user2@example.com", password="password123"
        )

        self.quiz1_user1 = Quiz.objects.create(
            title="User1 Quiz 1",
            description="Desc 1",
            video_url="https://www.youtube.com/watch?v=AAAAAAA1111",
            owner=self.user1,
        )
        self.quiz2_user1 = Quiz.objects.create(
            title="User1 Quiz 2",
            description="Desc 2",
            video_url="https://www.youtube.com/watch?v=BBBBBBB2222",
            owner=self.user1,
        )

        self.quiz_user2 = Quiz.objects.create(
            title="User2 Quiz",
            description="Desc 3",
            video_url="https://www.youtube.com/watch?v=CCCCCCC3333",
            owner=self.user2,
        )

        Question.objects.create(
            quiz=self.quiz1_user1,
            question_title="Q1",
            question_options=["A", "B", "C", "D"],
            answer="A",
        )

        Question.objects.create(
            quiz=self.quiz_user2,
            question_title="Q2",
            question_options=["A", "B", "C", "D"],
            answer="B",
        )

        self.list_url = "/api/quizzes/"
        self.detail_url_user1 = f"/api/quizzes/{self.quiz1_user1.id}/"
        self.detail_url_user2 = f"/api/quizzes/{self.quiz_user2.id}/"

    # ---- LIST ----

    def test_list_requires_authentication(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_returns_only_own_quizzes(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

        returned_ids = {item["id"] for item in response.data}
        self.assertSetEqual(
            returned_ids, {self.quiz1_user1.id, self.quiz2_user1.id}
        )

    # ---- RETRIEVE ----

    def test_retrieve_own_quiz(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.detail_url_user1)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.quiz1_user1.id)
        self.assertEqual(response.data["title"], self.quiz1_user1.title)

    def test_retrieve_foreign_quiz_returns_403(self):
        self.client.force_authenticate(self.user1)
        response = self.client.get(self.detail_url_user2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_retrieve_non_existing_quiz_returns_404(self):
        self.client.force_authenticate(self.user1)
        url = "/api/quizzes/999999/"
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # ---- PATCH ----

    def test_patch_title_of_own_quiz(self):
        self.client.force_authenticate(self.user1)
        payload = {"title": "Updated Title"}

        response = self.client.patch(self.detail_url_user1, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.quiz1_user1.refresh_from_db()
        self.assertEqual(self.quiz1_user1.title, "Updated Title")

    def test_patch_invalid_title_returns_400(self):
        self.client.force_authenticate(self.user1)
        payload = {"title": ""}

        response = self.client.patch(self.detail_url_user1, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("title", response.data)

    def test_patch_foreign_quiz_returns_403(self):
        self.client.force_authenticate(self.user1)
        payload = {"title": "Should Not Work"}

        response = self.client.patch(self.detail_url_user2, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # ---- DELETE ----

    def test_delete_own_quiz(self):
        self.client.force_authenticate(self.user1)

        response = self.client.delete(self.detail_url_user1)

        self.assertIn(
            response.status_code,
            (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK),
        )
        self.assertFalse(Quiz.objects.filter(id=self.quiz1_user1.id).exists())

    def test_delete_foreign_quiz_returns_403(self):
        self.client.force_authenticate(self.user1)

        response = self.client.delete(self.detail_url_user2)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertTrue(Quiz.objects.filter(id=self.quiz_user2.id).exists())

    def test_delete_requires_authentication(self):
        response = self.client.delete(self.detail_url_user1)

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
