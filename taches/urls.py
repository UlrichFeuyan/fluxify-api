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
    path('api/taches/initiateur/<int:initiateur_id>/', TachesByInitiateurListView.as_view(), name='taches_by_initiateur'),
    path('api/taches/executeur/<int:executeur_id>/', TachesByExecuteurListView.as_view(), name='taches_by_executeur'),
    path('api/taches/initiateur/<int:initiateur_id>/date/<str:date>/', TachesByInitiateurAndDateListView.as_view(), name='taches_by_initiateur_and_date'),
    path('api/taches/executeur/<int:executeur_id>/date/<str:date>/', TachesByExecuteurAndDateListView.as_view(), name='taches_by_executeur_and_date'),
    path('api/taches/cumulative_quota/initiateur/<int:initiateur_id>/date/<str:date>/', CumulativeQuotaByInitiateurView.as_view(), name='cumulative_quota_by_initiateur'),
    path('api/taches/cumulative_quota/executeur/<int:executeur_id>/date/<str:date>/', CumulativeQuotaByExecuteurView.as_view(), name='cumulative_quota_by_executeur'),
]
