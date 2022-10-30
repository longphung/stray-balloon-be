from django.contrib.auth.models import User, Group
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'groups']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']


class AuthResponseSerializer(serializers.Serializer):
    token = serializers.CharField()
    userId = serializers.IntegerField(min_value=0, source='user_id')
    email = serializers.EmailField()
    groups = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )
