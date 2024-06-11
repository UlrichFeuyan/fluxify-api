from django.urls import path, include
from .views import *
from rest_framework import routers

router = routers.SimpleRouter()

app_name = 'users'
urlpatterns = [
    path('', include(router.urls)),
    path('register', RegisterView.as_view()),
    path('login', LoginView.as_view()),
    path('user', UserView.as_view()),
    path('logout', LogoutView.as_view()),
    path('user_list', UserViewSet.as_view({'get': 'list'}), name='user-list'),
    path('user_list/<str:codeuser>/', UserViewSet.as_view({'get': 'retrieve'}), name='user-detail'),
]
