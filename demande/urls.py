from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
# router.register('activitesmission', ActivitesMissionViewset, basename='activitesmission')
router.register('demande', DemandeViewset, basename='demande')
router.register('typedemande', TypeDemandeViewset, basename='typedemande')


app_name = 'demande'
urlpatterns = [
    path('', include(router.urls)),
]
