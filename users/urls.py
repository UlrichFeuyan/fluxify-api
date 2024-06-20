from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()
router.register(r'profiles', ProfilViewSet, basename='profiles')
router.register(r'users', UserViewSet, basename='user')

app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('<str:codeuser>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
]
