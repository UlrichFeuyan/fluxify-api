from rest_framework import serializers
from .models import User, Profil
from drf_yasg.utils import swagger_serializer_method

class ProfilSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profil
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    profil = ProfilSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'codeuser', 'name', 'email', 'password', 'phone', 'profil']
        extra_kwargs = {
            'password': {'write_only': True, 'help_text': 'Enter a strong password'}
        }

    def create(self, validated_data):
        profil_data = validated_data.pop('profil', None)
        if profil_data:
            profil, created = Profil.objects.get_or_create(**profil_data)
            validated_data['profil'] = profil
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
