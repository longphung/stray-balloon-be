from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    user_id = serializers.IntegerField(min_value=0)
    email = serializers.EmailField()
