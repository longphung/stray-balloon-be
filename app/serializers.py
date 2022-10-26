from rest_framework import serializers
from app.models import Question, QuestionAnswer, SessionProgress, Session, SessionsQuestions


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = ['description', 'level', 'type', 'feedback']


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['question_id', 'description', 'is_correct']


class SessionProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionProgress
        fields = ['student_id', 'session_id', 'progress', 'attended']


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'start_time', 'end_time', 'instructor_id']


class SessionQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionsQuestions
        fields = ['session_id', 'question_id']
