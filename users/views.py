from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer
from .models import User
import jwt, datetime
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

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
                description="JWT Token",
                examples={
                    "application/json": {
                        "jwt": "your_jwt_token"
                    }
                }
            ),
            401: "Unauthorized"
        },
        operation_description="Authentifier un utilisateur, et retourner le Token"
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

        response = Response()

        response.set_cookie(key='jwt', value=token, httponly=True)
        response.data = {
            'jwt': token
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
