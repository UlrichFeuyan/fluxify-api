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

class DemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Demande
        fields = '__all__'


class TypeDemandeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TypeDemande
        fields = '__all__'


class CommentaireSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commentaire
        fields = '__all__'
