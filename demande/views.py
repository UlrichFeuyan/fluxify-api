import subprocess
from django.http import JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.core.exceptions import ImproperlyConfigured
from rest_framework.decorators import api_view, action, permission_classes
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.generics import RetrieveAPIView
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth import get_user_model, logout
from drf_yasg import openapi
from .serializers import *
from .models import *
from datetime import datetime
import os

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.http import HttpResponse
from django.db.models import Q

User = get_user_model()


"""
@permission_classes([IsAuthenticated])  # Exemple de permission, ajustez selon votre authentification
@api_view(['GET'])
def get_document_for_mission(request, mission_id):
    queryset = MissionDocument.objects.filter(idmission=mission_id).select_related('iddocument')
    documents = []
    if queryset:
        documents = [md.iddocument for md in queryset]
        serializer = DocumentSerializer(documents, many=True)
    return Response(serializer.data)

"""

class DemandeViewset(ModelViewSet):
    serializer_class = DemandeSerializer
    queryset = Demande.objects.all()

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
        
class TypeDemandeViewset(ModelViewSet):
    serializer_class = TypeDemandeSerializer
    queryset = TypeDemande.objects.all()


class CommentaireViewset(ModelViewSet):
    serializer_class = CommentaireSerializer
    queryset = Commentaire.objects.all()
