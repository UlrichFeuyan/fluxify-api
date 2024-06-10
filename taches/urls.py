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
    # Routes pour Statut
    path('statut/', StatutListCreate.as_view(), name='statut-list-create'),
    path('statut/<int:pk>/', StatutRetrieveUpdateDestroy.as_view(), name='statut-retrieve-update-destroy'),

    # Routes pour Tache
    path('tache/', TacheListCreate.as_view(), name='tache-list-create'),
    path('tache/<int:pk>/', TacheRetrieveUpdateDestroy.as_view(), name='tache-retrieve-update-destroy'),
]
