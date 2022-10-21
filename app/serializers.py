from rest_framework import serializers
from app.models import Question, QuestionAnswer, SessionProgress, Session, SessionsQuestions


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['description', 'level', 'type', 'feedback']


class QuestionAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['question_id', 'description', 'is_correct']


class SessionProgressSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SessionProgress
        fields = ['student_id', 'session_id', 'progress', 'attended']


class SessionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Session
        fields = ['start_time', 'end_time', 'instructor_id']


class SessionQuestionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SessionsQuestions
        fields = ['session_id', 'question_id']
