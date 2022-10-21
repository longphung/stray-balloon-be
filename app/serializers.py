from rest_framework import serializers
from app.models import Question, QuestionAnswer, SessionProgress


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
