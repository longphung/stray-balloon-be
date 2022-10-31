import json
from django.contrib.auth.models import User
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
    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['progress'] = json.loads(ret['progress'])
        for i, v in enumerate(ret['progress']):
            answer = QuestionAnswer.objects.filter(id=v['answer_taken']).first()
            if answer is None:
                ret['progress'][i]['is_correct'] = None
            ret['progress'][i]['is_correct'] = answer.is_correct

        return ret

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


class StudentReportInfoSerializer(serializers.ModelSerializer):
    sessionProgress = SessionProgressSerializer(many=True, source='session_progress')

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups', 'sessionProgress']
