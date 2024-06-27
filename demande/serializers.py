from rest_framework import serializers
from .models import Demande, DemandeValidation, Commentaire, TypeDemande
from users.serializers import UserSerializer


class DemandeValidationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DemandeValidation
        fields = ['id', 'user', 'status', 'created_at', 'updated_at', 'demande']


class TypeDemandeSerializer(serializers.ModelSerializer):
    validateurs_requis = UserSerializer(many=True, required=False)
    validateurs_optionnels = UserSerializer(many=True, required=False)

    class Meta:
        model = TypeDemande
        fields = ['id', 'nom', 'description', 'validateurs_requis', 'validateurs_optionnels', 'nombre_validations_min_requis', 'created_at', 'updated_at']


class DemandeSerializer(serializers.ModelSerializer):
    type_demande = TypeDemandeSerializer()
    initiateur = UserSerializer()
    validations = DemandeValidationSerializer(many=True, read_only=True)

    class Meta:
        model = Demande
        fields = ['id', 'type_demande', 'initiateur', 'status', 'active', 'created_at', 'updated_at', 'validations']


class CommentaireSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Commentaire
        fields = '__all__'
