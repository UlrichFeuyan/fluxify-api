import subprocess
from typing import Generic
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
from rest_framework import generics
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

"""

# VUE POUR STATUT.

class StatutViewset(ModelViewSet):
    serializer_class = StatutSerializer
    queryset = Statut.objects.all()

class StatutListCreate(generics.ListCreateAPIView):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer

class StatutRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer



#VUE POUR TACHE


class TacheViewset(ModelViewSet):
    serializer_class = TacheSerializer
    queryset = Tache.objects.all()

class TacheListCreate(generics.ListCreateAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer

class TacheRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer
