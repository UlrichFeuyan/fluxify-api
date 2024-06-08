from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
# router.register('activitesmission', ActivitesMissionViewset, basename='activitesmission')
router.register('tache', TacheViewset, basename='tache')
router.register('statut', StatutViewset, basename='statut')


app_name = 'demande'
urlpatterns = [
    path('', include(router.urls)),
]
