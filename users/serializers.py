from rest_framework import serializers
from .models import User
from drf_yasg.utils import swagger_serializer_method

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'codeuser', 'name', 'email', 'password']
        extra_kwargs = {
            'password': {'write_only': True, 'help_text': 'Enter a strong password'}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
