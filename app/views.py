from rest_framework import viewsets, permissions, views
from drf_spectacular import utils
from rest_framework.response import Response
from app.models import Question, QuestionAnswer, SessionProgress, Session, SessionsQuestions
from app.serializers import QuestionSerializer, QuestionAnswerSerializer, SessionProgressSerializer, SessionSerializer, \
    SessionQuestionsSerializer, AnswersOfQuestionsSerializer


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


class SessionViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching SessionProgress data
    """
    queryset = Session.objects.all().order_by('id')
    serializer_class = SessionSerializer
    permission_classes = [permissions.IsAuthenticated]


class SessionsQuestionsViewSet(viewsets.ModelViewSet):
    """
    API endpoint for fetching SessionProgress data
    """
    queryset = SessionsQuestions.objects.all().order_by('session_id')
    serializer_class = SessionQuestionsSerializer
    permission_classes = [permissions.IsAuthenticated]


class AnswersOfQuestionsViews(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = AnswersOfQuestionsSerializer

    @utils.extend_schema(
        parameters=[
            utils.OpenApiParameter(name='id', description='Question ID', required=True, type=str)
        ]
    )
    def get(self, request):
        question_id = request.query_params['id']
        question = Question.objects.filter(id=question_id).first()
        if question is None:
            return Response(
                {}, status=404
            )
        question.answers = QuestionAnswer.objects.filter(question_id=question_id)
        serializer = AnswersOfQuestionsSerializer(question)
        print(serializer.data)
        return Response(
            serializer.data
        )
