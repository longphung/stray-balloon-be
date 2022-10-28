from rest_framework import serializers
from app.models import Question, QuestionAnswer, SessionProgress, Session, SessionsQuestions


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'


class QuestionAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionAnswer
        fields = '__all__'


class SessionProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionProgress
        fields = '__all__'


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = '__all__'


class SessionQuestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionsQuestions
        fields = '__all__'


class AnswersOfQuestionsSerializer(serializers.ModelSerializer):
    answers = QuestionAnswerSerializer(many=True)

    # def get_answers(self, instance):
    class Meta:
        model = Question
        fields = '__all__'
