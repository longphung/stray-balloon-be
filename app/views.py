from rest_framework import viewsets, permissions
from app.models import Question, QuestionAnswer, SessionProgress
from app.serializers import QuestionSerializer, QuestionAnswerSerializer, SessionProgressSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching Question data
    """
    queryset = Question.objects.all().order_by('level')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionAnswersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching QuestionAnswer data
    """
    queryset = QuestionAnswer.objects.all().order_by('question_id')
    serializer_class = QuestionAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]


class SessionProgressViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching SessionProgress data
    """
    queryset = SessionProgress.objects.all().order_by('student_id')
    serializer_class = SessionProgressSerializer
    permission_classes = [permissions.IsAuthenticated]
