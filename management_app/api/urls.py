from django.urls import path, include
from rest_framework import routers
from .views import QuizCreateView, QuizViewSet

router = routers.SimpleRouter()
router.register(r'quizzes', QuizViewSet, basename='quiz')

urlpatterns = [
    path('createQuiz/', QuizCreateView.as_view(), name='create-quiz'),
    path('', include(router.urls)),
]