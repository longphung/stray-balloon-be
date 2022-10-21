from rest_framework import serializers
from app.models import Question, QuestionAnswer


class QuestionSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Question
        fields = ['description', 'level', 'type', 'feedback']


class QuestionAnswerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = ['question_id', 'description', 'is_correct']
