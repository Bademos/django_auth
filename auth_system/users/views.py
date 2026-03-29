from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer,
    UserUpdateSerializer, UserResponseSerializer
)
from .services import AuthService
from rest_framework import generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .models import User
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.renderers import JSONRenderer
from django.middleware.csrf import get_token

class RegisterView(APIView):
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({
                'message': 'User registered successfully',
                'user': UserResponseSerializer(user).data
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            token, user = AuthService.login(
                serializer.validated_data['email'],
                serializer.validated_data['password']
            )
            if token:
                response = Response({
                    'message': 'Login successful',
                    'token': token,
                    'user': UserResponseSerializer(user).data
                })
                response.set_cookie('auth_token', token, httponly=True)
                return response
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):

    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


    def post(self, request):
        print("hello")
        token = request.COOKIES.get('auth_token')
        auth_header = request.headers.get('Authorization', '')
        if token:
            AuthService.logout(token)
            print("logout is ok")
        print(token)
        response = Response({'message': 'Logged out successfully'})
        response.delete_cookie('auth_token')
        return response


class ProfileView(APIView):
    def get(self, request):
        user = request.user
        if not user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(UserResponseSerializer(user).data)

    def put(self, request):
        user = request.user
        if not user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(UserResponseSerializer(user).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteAccountView(APIView):
    def post(self, request):
        user = request.user
        if not user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        user.is_active = False
        user.save()

        token = request.COOKIES.get('auth_token')
        if token:
            AuthService.logout(token)

        response = Response({'message': 'Account deleted successfully'})
        response.delete_cookie('auth_token')
        return response
# Create your views here.
class UserListView(generics.ListAPIView):
    """
    Список всех пользователей (только для администраторов)
    """
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserResponseSerializer
    permission_classes = [IsAuthenticated]


class TestAuthView(APIView):
    renderer_classes = [JSONRenderer]  # 👈 ВАЖНО!

    def get(self, request):
        if request.user and request.user.is_authenticated:
            return Response({
                'authenticated': True,
                'user_id': request.user.id,
                'user_email': request.user.email,
            })
        return Response({
            'authenticated': False,
            'message': 'No authenticated user'
        })

class GetCSRFTokenView(APIView):
    def get(self, request):
        csrf_token = get_token(request)
        return Response({'csrf_token': csrf_token})