from .models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):
        user = User.objects.create_user(
            email = validated_data['email'],
            password = validated_data['password'],
            name = validated_data['name']
        )
        return user
    class Meta:
        model=User
        fields=['email', 'password', 'name']
