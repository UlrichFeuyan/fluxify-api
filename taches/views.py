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
from django.db.models import Sum
from drf_yasg import openapi
from .serializers import *
from .models import *
from datetime import datetime
import os
if os.name != 'nt':
    import pwd
import hashlib

from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Prefetch
from django.http import HttpResponse
from django.db.models import Q

User = get_user_model()


# VUE POUR STATUT.

#class StatutViewset(ModelViewSet):
#    serializer_class = StatutSerializer
#    queryset = Statut.objects.all()

class StatutListCreate(generics.ListCreateAPIView):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer

class StatutRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Statut.objects.all()
    serializer_class = StatutSerializer



#VUE POUR TACHE
#class TacheViewset(ModelViewSet):
#    serializer_class = TacheSerializer
#    queryset = Tache.objects.all()

class TacheListCreate(generics.ListCreateAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer

class TacheRetrieveUpdateDestroy(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tache.objects.all()
    serializer_class = TacheSerializer

class TachesByInitiateurListView(generics.ListAPIView):
    serializer_class = TacheSerializer

    def get_queryset(self):
        initiateur_id = self.kwargs['initiateur_id']
        initiateur = get_object_or_404(User, id=initiateur_id)
        return Tache.objects.filter(initiateur=initiateur)

class TachesByExecuteurListView(generics.ListAPIView):
    serializer_class = TacheSerializer

    def get_queryset(self):
        executeur_id = self.kwargs['executeur_id']
        executeur = get_object_or_404(User, id=executeur_id)
        return Tache.objects.filter(executeur=executeur)
    
class TachesByInitiateurAndDateListView(generics.ListAPIView):
    serializer_class = TacheSerializer

    def get_queryset(self):
        initiateur_id = self.kwargs['initiateur_id']
        date_str = self.kwargs['date']
        initiateur = get_object_or_404(User, id=initiateur_id)
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return Tache.objects.filter(initiateur=initiateur, date_debut_tache__date=date)

class TachesByExecuteurAndDateListView(generics.ListAPIView):
    serializer_class = TacheSerializer

    def get_queryset(self):
        executeur_id = self.kwargs['executeur_id']
        date_str = self.kwargs['date']
        executeur = get_object_or_404(User, id=executeur_id)
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return Tache.objects.filter(executeur=executeur, date_debut_tache__date=date)
    

class CumulativeQuotaByInitiateurView(APIView):
    def get(self, request, initiateur_id, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        initiateur = get_object_or_404(User, id=initiateur_id)
        
        # Filter tasks by date and by initiateur
        taches_initiateur = Tache.objects.filter(initiateur=initiateur, date_debut_tache__date=date_obj)
        
        # Sum the quotas
        quota_initiateur = taches_initiateur.aggregate(Sum('quota'))['quota__sum'] or 0
        
        return Response({'date': date, 'initiateur_id': initiateur_id, 'cumulative_quota': quota_initiateur})

class CumulativeQuotaByExecuteurView(APIView):
    def get(self, request, executeur_id, date):
        date_obj = datetime.strptime(date, '%Y-%m-%d')
        executeur = get_object_or_404(User, id=executeur_id)
        
        # Filter tasks by date and by executeur
        taches_executeur = Tache.objects.filter(executeur=executeur, date_debut_tache__date=date_obj)
        
        # Sum the quotas
        quota_executeur = taches_executeur.aggregate(Sum('quota'))['quota__sum'] or 0
        
        return Response({'date': date, 'executeur_id': executeur_id, 'cumulative_quota': quota_executeur})