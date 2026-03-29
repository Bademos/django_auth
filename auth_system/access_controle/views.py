from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Role, BusinessElement, AccessRoleRule, UserRole
from .serializers import (
    RoleSerializer, BusinessElementSerializer,
    AccessRoleRuleSerializer, UserRoleSerializer
)
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .permissions import AccessChecker

class RoleListView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        # Проверка прав админа
        if not AccessChecker.check_permission(request.user, 'access_control', 'read'):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        roles = Role.objects.all()
        serializer = RoleSerializer(roles, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not AccessChecker.check_permission(request.user, 'access_control', 'create'):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        serializer = RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AccessRuleListView(APIView):
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get(self, request):
        if not AccessChecker.check_permission(request.user, 'access_control', 'read'):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        rules = AccessRoleRule.objects.all()
        serializer = AccessRoleRuleSerializer(rules, many=True)
        return Response(serializer.data)

    def post(self, request):
        if not AccessChecker.check_permission(request.user, 'access_control', 'create'):
            return Response({'error': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AccessRoleRuleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
