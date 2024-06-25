from django.urls import path, include
from .views import DemandeViewSet, DemandeValidationViewSet, CommentaireViewSet, TypeDemandeViewset
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'demandes', DemandeViewSet, basename='demande')
router.register(r'validations', DemandeValidationViewSet, basename='demandevalidation')
router.register(r'commentaires', CommentaireViewSet, basename='commentaire')
router.register(r'types', TypeDemandeViewset, basename='typedemande')

app_name = 'demande'
urlpatterns = [
    path('', include(router.urls)),
]
