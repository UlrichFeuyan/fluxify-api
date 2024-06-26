from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
# router.register('activitesmission', ActivitesMissionViewset, basename='activitesmission')
#router.register('tache', TacheViewset, basename='tache')
#router.register('statut', StatutViewset, basename='statut')


app_name = 'tache'
urlpatterns = [
    path('', include(router.urls)),
    # Routes pour Statut
    path('statut/', StatutListCreate.as_view(), name='statut-list-create'),
    path('statut/<int:pk>/', StatutRetrieveUpdateDestroy.as_view(), name='statut-retrieve-update-destroy'),

    # Routes pour Tache
    path('tache/', TacheListCreate.as_view(), name='tache-list-create'),
    path('tache/<int:pk>/', TacheRetrieveUpdateDestroy.as_view(), name='tache-retrieve-update-destroy'),

    path('api/taches/journaliere/initiateur/<str:initiateur_codeuser>/', TachesByInitiateurListView.as_view(), name='taches_by_initiateur'),
    path('api/taches/journaliere/executeur/<str:executeur_codeuser>/', TachesByExecuteurListView.as_view(), name='taches_by_executeur'),
    
    path('api/taches/initiateur/<str:initiateur_codeuser>/', TachesByInitiateurAndDateListView.as_view(), name='taches_by_initiateur_and_date'),
    path('api/taches/executeur/<str:executeur_codeuser>/', TachesByExecuteurAndDateListView.as_view(), name='taches_by_executeur_and_date'),

    path('api/taches/quota_journalier/initiateur/<str:initiateur_codeuser>/', CumulativeQuotaByInitiateurView.as_view(), name='cumulative_quota_by_initiateur'),
    path('api/taches/quota_journalier/executeur/<str:executeur_codeuser>/', CumulativeQuotaByExecuteurView.as_view(), name='cumulative_quota_by_executeur'),
]

