from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Role, User
from . import serializers
from notes_management import serializers as gs
# Create your views here.

class RoleView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        responses={200: serializers.RoleReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request):
        """
        Get All Roles
        """
        roles_queryset = Role.get_active()
        if roles_queryset.exists():
            serialized_data = serializers.RoleSerializer(roles_queryset, many=True)
            return Response({'status': status.HTTP_200_OK, 'detail': 'Success', 'metadata':serialized_data.data})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Roles Not Found. Please Create a Role', 'metadata':[]},
                            status=status.HTTP_404_NOT_FOUND)
        
        
    @swagger_auto_schema(
        request_body=serializers.RoleSerializer,
        responses={201: serializers.RoleSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(),
                   401:gs.Generic401Serializer()}
    )
    def post(self, request):
        """
        Create New Role
        """
        if not request.user.is_superuser:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'detail': "Only SuperUser Can Create Role", 'data':[]}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_201_CREATED, 'detail': "Role Created.", 'data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': serializer.errors, 'data':[]}, status=status.HTTP_400_BAD_REQUEST)


class SingleRoleView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        responses={200: serializers.RoleReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request, pk):
        """
        Get Role By Primary Key
        """
        try:
            role_queryset = Role.objects.get(pk=pk, is_active=True, is_deleted=False)
        except Role.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Role Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        role_serializer = serializers.RoleSerializer(role_queryset)
        return Response({'status': status.HTTP_200_OK, 'detail': 'Role successfully retrieved.', 'metadata':role_serializer.data})
    
    @swagger_auto_schema(
        request_body=serializers.RoleSerializer,
        responses={200: serializers.RoleReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(), 401:gs.Generic401Serializer()}
    )
    def put(self, request, pk):
        """
        Update Role By Primary Key
        """
        try:
            role_queryset = Role.objects.get(pk=pk, is_active=True, is_deleted=False)
        except Role.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Role Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        if not request.user.is_superuser:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'detail': "Only SuperUser Can Update Role", 'data':[]}, status=status.HTTP_401_UNAUTHORIZED)
        role_serializer = serializers.RoleSerializer(role_queryset, data=request.data, partial=True)
        if role_serializer.is_valid():
            role_serializer.save()
            return Response({'status': status.HTTP_200_OK, 'detail': 'Role successfully updated.', 'metadata':role_serializer.data})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'Unable to update Role.', 'metadata':role_serializer.errors})
    
    @swagger_auto_schema(
        responses={200: serializers.RoleReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(), 401:gs.Generic401Serializer()}
    )
    def delete(self, request, pk):
        """
        Soft Delete Role By Primary Key
        """
        try:
            role_queryset = Role.objects.get(pk=pk, is_active=True, is_deleted=False)
        except Role.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Role Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        if not request.user.is_superuser:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'detail': "Only SuperUser Can Delete Role", 'data':[]}, status=status.HTTP_401_UNAUTHORIZED)
        role_queryset.is_deleted = True
        role_queryset.is_active = False
        role_queryset.save()
        return Response({'status': status.HTTP_200_OK, 'detail': 'Role successfully Deleted.', 'metadata':[]})


class UserView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        responses={200: serializers.UserReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(), 401:gs.Generic401Serializer()}
    )
    def get(self, request):
        """
        Get All Users
        """
        user_queryset = User.get_active()
        if user_queryset.exists():
            user_queryset = serializers.UserSerializer.setup_eager_loading(user_queryset)
            serialized_data = serializers.UserSerializer(user_queryset, many=True)
            return Response({'status': status.HTTP_200_OK, 'detail': 'Success', 'metadata':serialized_data.data})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'User Not Found. Please Create a User', 'metadata':[]},
                            status=status.HTTP_404_NOT_FOUND)
        

class SignUpView(APIView):
    permission_classes = (IsAuthenticated, )
    
    @swagger_auto_schema(
        request_body=serializers.UserSerializerCreate,
        responses={201: serializers.UserReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(), 401:gs.Generic401Serializer()}
    )
    def post(self, request):
        """
        Create New User
        """
        serializer = serializers.UserSerializerCreate(data=request.data)
        if serializer.is_valid():
            saved_instance = serializer.save()
            return_serializer = serializers.UserSerializer(saved_instance)
            return Response({'status': status.HTTP_201_CREATED, 'detail': "User Created.", 'data':return_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': serializer.errors, 'data':[]}, status=status.HTTP_400_BAD_REQUEST)


class SingleUserView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        responses={200: serializers.UserReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request, pk):
        """
        Get User By Primary Key
        """
        try:
            user_queryset = User.objects.get(pk=pk, is_active=True, is_deleted=False)
        except User.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested User Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        user_serializer = serializers.UserSerializer(user_queryset)
        return Response({'status': status.HTTP_200_OK, 'detail': 'User Details successfully retrieved.', 'metadata':user_serializer.data})
    
    @swagger_auto_schema(
        request_body=serializers.UserSerializerCreate,
        responses={200: serializers.UserReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(), 401:gs.Generic401Serializer()}
    )
    def put(self, request, pk):
        """
        Update User By Primary Key
        """
        try:
            user_queryset = User.objects.get(pk=pk, is_active=True, is_deleted=False)
        except User.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested User Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)

        if request.user.id != pk:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'detail': "Not Authorized to Update Other User's Information", 'data':[]}, status=status.HTTP_401_UNAUTHORIZED)
        user_serializer = serializers.UserSerializerCreate(user_queryset, data=request.data, partial=True)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response({'status': status.HTTP_200_OK, 'detail': 'User successfully updated.', 'metadata':user_serializer.data})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'Unable to update User.', 'metadata':user_serializer.errors})
    
    @swagger_auto_schema(
        responses={200: serializers.UserReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(), 401:gs.Generic401Serializer()}
    )
    def delete(self, request, pk):
        """
        Soft Delete User By Primary Key
        """
        try:
            user_queryset = User.objects.get(pk=pk, is_active=True, is_deleted=False)
        except User.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested User Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        if request.user.id != pk:
            return Response({'status': status.HTTP_401_UNAUTHORIZED, 'detail': "Not Authorized to Delete Other User", 'data':[]}, status=status.HTTP_401_UNAUTHORIZED)
        user_queryset.is_deleted = True
        user_queryset.is_active = False
        user_queryset.save()
        return Response({'status': status.HTTP_200_OK, 'detail': 'User successfully Deleted.', 'metadata':[]})

