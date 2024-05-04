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
import pwd
import hashlib

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

class ActivitesMissionViewset(ModelViewSet):
    serializer_class = ActivitesMissionSerializer
    queryset = ActivitesMission.objects.all()
"""
