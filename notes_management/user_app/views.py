from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema

from .models import Role
from . import serializers
from notes_management import serializers as gs
# Create your views here.

class RoleView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        responses={200: serializers.RoleReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request):
        roles_queryset = Role.get_active()
        print(roles_queryset)
        if roles_queryset.exists():
            serialized_data = serializers.RoleSerializer(roles_queryset, many=True)
            return Response({'status': status.HTTP_200_OK, 'detail': 'Success', 'metadata':serialized_data.data})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Roles Not Found. Please Create a Role', 'metadata':[]},
                            status=status.HTTP_404_NOT_FOUND)
        
    @swagger_auto_schema(
        request_body=serializers.RoleSerializer,
        responses={201: serializers.RoleSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def post(self, request):
        serializer = serializers.RoleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_201_CREATED, 'detail': "Role Created.", 'data':[serializer.data]}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': serializer.errors, 'data':[]}, status=status.HTTP_400_BAD_REQUEST)

        
    