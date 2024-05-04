from django.urls import path, include
from rest_framework import routers
from .views import *

router = routers.SimpleRouter()
# router.register('activitesmission', ActivitesMissionViewset, basename='activitesmission')


app_name = 'account'
urlpatterns = [
    path('', include(router.urls)),
]
