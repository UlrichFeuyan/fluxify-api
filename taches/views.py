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
from datetime import datetime, timedelta
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

    def get(self, request, *args, **kwargs):
        try:
            initiateur_codeuser = self.kwargs['initiateur_codeuser']
            if not isinstance(initiateur_codeuser, str):
                return Response({"error": "Mauvais type de donnée entrée"}, status=status.HTTP_400_BAD_REQUEST)

            initiateur = get_object_or_404(User, codeuser=initiateur_codeuser)
            queryset = Tache.objects.filter(initiateur_id=initiateur.id)
            if not queryset.exists():
                return Response({"error": "Aucune tâche trouvée"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Initiateur not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TachesByExecuteurListView(generics.ListAPIView):
    serializer_class = TacheSerializer

    def get(self, request, *args, **kwargs):
        try:
            executeur_codeuser = self.kwargs['executeur_codeuser']
            if not isinstance(executeur_codeuser, str):
                return Response({"error": "Mauvais type de donnée entrée"}, status=status.HTTP_400_BAD_REQUEST)

            executeur = get_object_or_404(User, codeuser=executeur_codeuser)
            queryset = Tache.objects.filter(executeur_id=executeur.id)
            if not queryset.exists():
                return Response({"error": "Aucune tâche trouvée"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Executeur not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
    
class TachesByInitiateurAndDateListView(generics.ListAPIView):
    serializer_class = TacheSerializer

    def get(self, request, *args, **kwargs):
        try:
            initiateur_codeuser = self.kwargs['initiateur_codeuser']
            if not isinstance(initiateur_codeuser, str):
                return Response({"error": "Mauvais type de donnée entrée"}, status=status.HTTP_400_BAD_REQUEST)

            initiateur = get_object_or_404(User, codeuser=initiateur_codeuser)
            today = datetime.today().date()
            queryset = Tache.objects.filter(initiateur_id=initiateur.id, date_debut_tache__date=today)
            if not queryset.exists():
                return Response({"error": "Aucune tâche trouvée"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Initiateur not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TachesByExecuteurAndDateListView(generics.ListAPIView):
    serializer_class = TacheSerializer

    def get(self, request, *args, **kwargs):
        try:
            executeur_codeuser = self.kwargs['executeur_codeuser']
            if not isinstance(executeur_codeuser, str):
                return Response({"error": "Mauvais type de donnée entrée"}, status=status.HTTP_400_BAD_REQUEST)

            executeur = get_object_or_404(User, codeuser=executeur_codeuser)
            today = datetime.today().date()
            queryset = Tache.objects.filter(executeur_id=executeur.id, date_debut_tache__date=today)
            if not queryset.exists():
                return Response({"error": "Aucune tâche trouvée"}, status=status.HTTP_404_NOT_FOUND)
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "Executeur not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)    

class CumulativeQuotaByInitiateurView(APIView):
    def get(self, request, initiateur_codeuser):
        try:
            if not isinstance(initiateur_codeuser, str):
                return Response({"error": "Mauvais type de donnée entrée"}, status=status.HTTP_400_BAD_REQUEST)

            initiateur = get_object_or_404(User, codeuser=initiateur_codeuser)
            today_start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)

            # Filter tasks by date range and by initiateur
            taches_initiateur = Tache.objects.filter(initiateur_id=initiateur.id, date_debut_tache__gte=today_start, date_debut_tache__lt=today_end)
            print(today_start)
            
            # Sum the quotas
            quota_initiateur = taches_initiateur.aggregate(Sum('quota'))['quota__sum'] or 0
            return Response({'initiateur_codeuser': initiateur_codeuser, 'cumulative_quota': quota_initiateur})
        except User.DoesNotExist:
            return Response({"error": "Initiateur not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class CumulativeQuotaByExecuteurView(APIView):
    def get(self, request, executeur_codeuser):
        try:
            if not isinstance(executeur_codeuser, str):
                return Response({"error": "Mauvais type de donnée entrée"}, status=status.HTTP_400_BAD_REQUEST)

            executeur = get_object_or_404(User, codeuser=executeur_codeuser)
            today_start = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            today_end = today_start + timedelta(days=1)

            # Filter tasks by date range and by executeur
            taches_executeur = Tache.objects.filter(executeur_id=executeur.id, date_debut_tache__gte=today_start, date_debut_tache__lt=today_end)
            
            # Sum the quotas
            quota_executeur = taches_executeur.aggregate(Sum('quota'))['quota__sum'] or 0
            return Response({'executeur_codeuser': executeur_codeuser, 'cumulative_quota': quota_executeur})
        except User.DoesNotExist:
            return Response({"error": "Executeur not found"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

