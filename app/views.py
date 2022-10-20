from rest_framework import viewsets, permissions
from app.models import Question, QuestionAnswer
from app.serializers import QuestionSerializer, QuestionAnswerSerializer


class QuestionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching Question data
    """
    queryset = Question.objects.all().order_by('level')
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAuthenticated]


class QuestionAnswersViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching Question data
    """
    queryset = QuestionAnswer.objects.all().order_by('question_id')
    serializer_class = QuestionAnswerSerializer
    permission_classes = [permissions.IsAuthenticated]
