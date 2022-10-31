from rest_framework import viewsets, permissions, views
from django.contrib.auth.models import User, Group
from drf_spectacular import utils
from rest_framework.response import Response
from quickstart import serializers
from app.models import Question, QuestionAnswer, SessionProgress, Session, SessionsQuestions
from app.serializers import QuestionSerializer, QuestionAnswerSerializer, SessionProgressSerializer, SessionSerializer, \
    SessionQuestionsSerializer, AnswersOfQuestionsSerializer, StudentReportInfoSerializer


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
        return Response(
            serializer.data
        )


class SessionProgressOfStudent(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = SessionProgressSerializer

    @utils.extend_schema(
        parameters=[
            utils.OpenApiParameter(name='session_id', description='Session ID', required=True, type=int),
            utils.OpenApiParameter(name='student_id', description='Student ID', required=True, type=int)
        ],
        responses={
            200: SessionProgressSerializer,
            404: {},
        },
    )
    def get(self, request):
        session_id = request.query_params['session_id']
        student_id = request.query_params['student_id']
        session_progress = SessionProgress.objects.filter(session_id=session_id, student_id=student_id).first()
        if session_progress is None:
            return Response(
                {}, status=404
            )
        serializer = SessionProgressSerializer(session_progress)
        return Response(
            serializer.data
        )


class Students(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = serializers.UserSerializer

    @utils.extend_schema(
        responses={
            200: serializers.UserSerializer,
            404: {},
        },
    )
    def get(self, request):
        student_group = Group.objects.filter(name='students').first()
        user = User.objects.filter(groups=student_group)
        if user is None:
            return Response({}, status=404)
        serializer = serializers.UserSerializer(user, many=True)
        return Response(serializer.data)


class StudentReportInfo(views.APIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = [StudentReportInfoSerializer]

    @utils.extend_schema(
        parameters=[
            utils.OpenApiParameter(name='username', description='Student Username', required=True, type=str),
        ],
        responses={
            200: StudentReportInfoSerializer,
            404: {},
        },
    )
    def get(self, request):
        username = request.query_params['username']
        student_group = Group.objects.filter(name='students').first()
        user = User.objects.filter(groups=student_group, username=username).first()
        if user is None:
            return Response({}, status=404)
        session_progress = SessionProgress.objects.filter(student_id=user)
        print(session_progress)
        ret = user
        ret.session_progress = session_progress
        serializer = StudentReportInfoSerializer(ret)
        return Response(serializer.data)
