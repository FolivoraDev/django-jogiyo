from django.contrib.auth import get_user_model
from rest_framework import serializers

from members.models import User


class UserSerializer(serializers.ModelSerializer):

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'email', 'phone_number', 'nick_name')
        write_only_fields = ('password',)
