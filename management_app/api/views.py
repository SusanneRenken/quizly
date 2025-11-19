from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from management_app.models import Quiz
from .serializers import QuizSerializer, CreateQuizSerializer

class QuizCreateView(generics.CreateAPIView):
    serializer_class = CreateQuizSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(QuizSerializer(instance).data, status=status.HTTP_201_CREATED)

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer
    queryset = Quiz.objects.all()  # later: set request.user filter
