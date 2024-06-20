from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed, NotFound
from rest_framework.generics import ListAPIView
from .serializers import UserSerializer, ProfilSerializer
from .models import User, Profil
import jwt, datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class ProfilViewSet(ModelViewSet):
    queryset = Profil.objects.all()
    serializer_class = ProfilSerializer

class RegisterView(APIView):
    @swagger_auto_schema(
        request_body=UserSerializer,
        responses={201: UserSerializer},
        operation_description="Créer un utilisateur"
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

class LoginView(APIView):
    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'codeuser': openapi.Schema(type=openapi.TYPE_STRING, description='codeuser'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description='Password')
            }
        ),
        responses={
            200: openapi.Response(
                description="JWT Token and user data",
                examples={
                    "application/json": {
                        "jwt": "your_jwt_token",
                        "user": {
                            "id": 1,
                            "codeuser": "USXXX",
                            "name": "User Name",
                            "email": "user@example.com"
                        }
                    }
                }
            ),
            401: "Unauthorized"
        },
        operation_description="Authentifier un utilisateur, et retourner le Token avec les données de l'utilisateur"
    )
    def post(self, request):
        codeuser = request.data['codeuser']
        password = request.data['password']

        user = User.objects.filter(codeuser=codeuser).first()

        if user is None:
            raise AuthenticationFailed('Utilisateur introuvable !')

        if not user.check_password(password):
            raise AuthenticationFailed('Mot de passe incorrect !')

        payload = {
            'id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat': datetime.datetime.utcnow()
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        user_data = UserSerializer(user).data  # Sérialiser les données de l'utilisateur

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token,
            'user': user_data  # Inclure les données de l'utilisateur dans la réponse
        }

        return response

class UserView(APIView):
    @swagger_auto_schema(
        responses={
            200: UserSerializer,
            401: "Unauthenticated"
        },
        operation_description="Récupérer les données de l'utilisateur authentifié"
    )
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)

        return Response(serializer.data)

class LogoutView(APIView):
    @swagger_auto_schema(
        responses={
            200: "Logout successfully"
        },
        operation_description="Logout user by deleting JWT cookie"
    )
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Logout successfully'
        }
        return response

class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @swagger_auto_schema(
        operation_description="Lister les utilisateurs",
        responses={200: UserSerializer(many=True)}
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Récupérer un utilisateur par son codeuser",
        responses={200: UserSerializer, 404: "User not found"},
        manual_parameters=[
            openapi.Parameter(
                'codeuser',
                openapi.IN_PATH,
                description="Code utilisateur",
                type=openapi.TYPE_STRING
            )
        ]
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def get_object(self):
        queryset = self.get_queryset()
        codeuser = self.kwargs.get('codeuser')
        user = queryset.filter(codeuser=codeuser).first()
        if user is None:
            raise NotFound("User not found")
        return user

    @swagger_auto_schema(
        operation_description="Mettre à jour un utilisateur",
        request_body=UserSerializer,
        responses={200: UserSerializer, 404: "User not found"}
    )
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Mettre à jour partiellement un utilisateur",
        request_body=UserSerializer,
        responses={200: UserSerializer, 404: "User not found"}
    )
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return self.update(request, *args, **kwargs)