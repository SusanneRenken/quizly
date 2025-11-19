from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, generics, viewsets
from rest_framework.response import Response
from management_app.models import Quiz
from .serializers import QuizSerializer, CreateQuizSerializer, QuizWithTimestampsSerializer
from .permissions import IsQuizOwner

class QuizCreateView(generics.CreateAPIView):
    serializer_class = CreateQuizSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = serializer.save()
        return Response(QuizWithTimestampsSerializer(instance).data, status=status.HTTP_201_CREATED)

class QuizViewSet(viewsets.ModelViewSet):
    serializer_class = QuizSerializer    
    permission_classes = [IsAuthenticated, IsQuizOwner]

    def get_queryset(self):
        if self.action == "list":
            return Quiz.objects.filter(owner=self.request.user).order_by("-created_at")
        return Quiz.objects.all()