from django.contrib.auth import get_user_model, password_validation
from rest_framework import serializers
from .models import *

User = get_user_model()

"""
class ActivitesMissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActivitesMission
        fields = '__all__'
"""

class StatutSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statut
        fields = '__all__'


class TacheSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tache
        fields = '__all__'

