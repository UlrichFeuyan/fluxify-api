from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from .models import Demande, DemandeValidation, Commentaire, TypeDemande
from .serializers import DemandeSerializer, DemandeValidationSerializer, CommentaireSerializer, TypeDemandeSerializer

class DemandeViewSet(ModelViewSet):
    queryset = Demande.objects.all()
    serializer_class = DemandeSerializer

    @swagger_auto_schema(
        operation_description="Récupérer les demandes initiées par un utilisateur",
        manual_parameters=[
            openapi.Parameter('codeuser', openapi.IN_PATH, description="Code utilisateur", type=openapi.TYPE_STRING)
        ],
        responses={200: DemandeSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='initiees-par/(?P<codeuser>[^/.]+)', url_name='initiees-par')
    def initiees_par(self, request, codeuser=None):
        demandes = Demande.objects.filter(initiateur__codeuser=codeuser)
        page = self.paginate_queryset(demandes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(demandes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Récupérer les demandes à valider par un utilisateur",
        manual_parameters=[
            openapi.Parameter('codeuser', openapi.IN_PATH, description="Code utilisateur", type=openapi.TYPE_STRING)
        ],
        responses={200: DemandeSerializer(many=True)}
    )
    @action(detail=False, methods=['get'], url_path='a-valider-par/(?P<codeuser>[^/.]+)', url_name='a-valider-par')
    def a_valider_par(self, request, codeuser=None):
        demandes = Demande.objects.filter(validateurs__codeuser=codeuser, active=True, status=0)
        page = self.paginate_queryset(demandes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(demandes, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Désactiver une demande",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la demande à désactiver", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="Demande désactivée avec succès",
                examples={
                    "application/json": {
                        "status": "demande désactivée"
                    }
                }
            ),
            404: openapi.Response(
                description="Demande non trouvée",
                examples={
                    "application/json": {
                        "error": "Demande non trouvée"
                    }
                }
            )
        },
        request_body=None  # Indique qu'il n'y a pas de corps de requête
    )
    @action(detail=True, methods=['post'], url_path='desactiver', url_name='desactiver')
    def desactiver(self, request, pk=None):
        try:
            demande = self.get_object()
            demande.active = False
            demande.save()
            return Response({'status': 'demande désactivée'}, status=status.HTTP_200_OK)
        except Demande.DoesNotExist:
            return Response({'error': 'Demande non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Activer une demande",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la demande à activer", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="Demande activée avec succès",
                examples={
                    "application/json": {
                        "status": "demande activée"
                    }
                }
            ),
            404: openapi.Response(
                description="Demande non trouvée",
                examples={
                    "application/json": {
                        "error": "Demande non trouvée"
                    }
                }
            )
        },
        request_body=None  # Indique qu'il n'y a pas de corps de requête
    )
    @action(detail=True, methods=['post'], url_path='activer', url_name='activer')
    def activer(self, request, pk=None):
        try:
            demande = self.get_object()
            demande.active = True
            demande.save()
            return Response({'status': 'demande activée'}, status=status.HTTP_200_OK)
        except Demande.DoesNotExist:
            return Response({'error': 'Demande non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Valider une demande",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la demande à valider", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de l'utilisateur validant"),
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Statut de validation (True pour valider, False pour rejeter)")
            }
        ),
        responses={
            200: openapi.Response(
                description="Validation de la demande mise à jour",
                examples={
                    "application/json": {
                        "status": "validation mise à jour"
                    }
                }
            ),
            404: openapi.Response(
                description="Demande non trouvée",
                examples={
                    "application/json": {
                        "error": "Demande non trouvée"
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['post'], url_path='valider', url_name='valider')
    def valider(self, request, pk=None):
        try:
            demande = self.get_object()
            user_id = request.data.get('user_id')
            status = request.data.get('status')
            validation = DemandeValidation.objects.get(demande=demande, user_id=user_id)
            validation.status = status
            validation.save()
            demande.evaluer_statut()
            return Response({'status': 'validation mise à jour'}, status=status.HTTP_200_OK)
        except Demande.DoesNotExist:
            return Response({'error': 'Demande non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        except DemandeValidation.DoesNotExist:
            return Response({'error': 'Validation non trouvée'}, status=status.HTTP_404_NOT_FOUND)

    @swagger_auto_schema(
        operation_description="Rejeter une demande",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID de la demande à rejeter", type=openapi.TYPE_INTEGER)
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'user_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID de l'utilisateur rejetant"),
                'status': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Statut de rejet (False pour rejeter)")
            }
        ),
        responses={
            200: openapi.Response(
                description="Rejet de la demande mis à jour",
                examples={
                    "application/json": {
                        "status": "rejet mis à jour"
                    }
                }
            ),
            404: openapi.Response(
                description="Demande non trouvée",
                examples={
                    "application/json": {
                        "error": "Demande non trouvée"
                    }
                }
            )
        }
    )
    @action(detail=True, methods=['post'], url_path='rejeter', url_name='rejeter')
    def rejeter(self, request, pk=None):
        try:
            demande = self.get_object()
            user_id = request.data.get('user_id')
            validation = DemandeValidation.objects.get(demande=demande, user_id=user_id)
            validation.status = False  # Rejeter la demande
            validation.save()
            demande.evaluer_statut()
            return Response({'status': 'rejet mis à jour'}, status=status.HTTP_200_OK)
        except Demande.DoesNotExist:
            return Response({'error': 'Demande non trouvée'}, status=status.HTTP_404_NOT_FOUND)
        except DemandeValidation.DoesNotExist:
            return Response({'error': 'Validation non trouvée'}, status=status.HTTP_404_NOT_FOUND)


class DemandeValidationViewSet(ModelViewSet):
    queryset = DemandeValidation.objects.all()
    serializer_class = DemandeValidationSerializer


class CommentaireViewSet(ModelViewSet):
    queryset = Commentaire.objects.all()
    serializer_class = CommentaireSerializer


class TypeDemandeViewset(ModelViewSet):
    serializer_class = TypeDemandeSerializer
    queryset = TypeDemande.objects.all()
