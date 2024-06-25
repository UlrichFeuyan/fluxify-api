from rest_framework import serializers

from users.models import Profil
from .models import Demande, DemandeValidation, Commentaire, TypeDemande
from users.serializers import UserSerializer, ProfilSerializer

class DemandeValidationSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = DemandeValidation
        fields = '__all__'

class TypeDemandeSerializer(serializers.ModelSerializer):
    profils_requis = ProfilSerializer(many=True, required=False)
    profils_optionnels = ProfilSerializer(many=True, required=False)

    class Meta:
        model = TypeDemande
        fields = '__all__'

    def create(self, validated_data):
        profils_requis_data = validated_data.pop('profils_requis', [])
        profils_optionnels_data = validated_data.pop('profils_optionnels', [])
        type_demande = TypeDemande.objects.create(**validated_data)

        if profils_requis_data:
            for profil_data in profils_requis_data:
                profil, created = Profil.objects.get_or_create(**profil_data)
                type_demande.profils_requis.add(profil)

        if profils_optionnels_data:
            for profil_data in profils_optionnels_data:
                profil, created = Profil.objects.get_or_create(**profil_data)
                type_demande.profils_optionnels.add(profil)

        return type_demande

class DemandeSerializer(serializers.ModelSerializer):
    type_demande = TypeDemandeSerializer()
    initiateur = UserSerializer()
    validations = DemandeValidationSerializer(many=True)

    class Meta:
        model = Demande
        fields = '__all__'

class CommentaireSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Commentaire
        fields = '__all__'
