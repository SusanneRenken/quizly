from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User, AnonymousUser

from quizzes_app.api.views import QuizViewSet
from quizzes_app.models import Quiz


class QuizViewSetQuerysetTests(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        # create a user and a quiz to ensure DB isn't empty
        self.user = User.objects.create_user(username="owner", password="pw")
        Quiz.objects.create(title="T", description="D", video_url="http://x", owner=self.user)

    def test_get_queryset_list_anonymous_returns_empty(self):
        request = self.rf.get("/")
        request.user = AnonymousUser()

        view = QuizViewSet()
        view.action = "list"
        view.request = request

        qs = view.get_queryset()
        # Should return an empty queryset for anonymous list requests
        self.assertEqual(qs.count(), 0)
