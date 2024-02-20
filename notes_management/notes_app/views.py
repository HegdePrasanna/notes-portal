from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotFound, NotAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Notes, NotesUser
from . import serializers
from notes_management import serializers as gs
# Create your views here.


class IsAuthorized(BasePermission):
    """
    Custom permission to only check authorization users in notes sharing.
    """

    def has_permission(self, request, view):
        """
        Check if the user making the request is authorized.
        """
        note_id = view.kwargs.get('note_id')
        try:
            is_present = NotesUser.objects.get(notes_id=note_id, user_id=request.user, is_active=True, is_deleted=False)
        except NotesUser.DoesNotExist:
            raise NotFound("Requested Note is not shared with the User")
        
        if request.method == "GET":
            if not is_present.can_read:
                raise PermissionDenied("You Do Not Permission to Read the Note")
        elif request.method == "PUT":
            if not is_present.can_edit:
                raise PermissionDenied("You Do Not Permission to Edit the Note")
        elif request.method == "DELETE":
            if not is_present.can_delete:
                raise PermissionDenied("You Do Not Permission to Delete the Note")
        else:
            return False

        return True
    

class NotesView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        responses={200: serializers.NoteReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request):
        """
        Get All Roles
        """
        notes_queryset = Notes.get_active()
        if notes_queryset.exists():
            serialized_data = serializers.NoteSerializer(notes_queryset, many=True)
            return Response({'status': status.HTTP_200_OK, 'detail': 'Success', 'metadata':serialized_data.data})
        else:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Note Not Found. Please Create a Note', 'metadata':[]},
                            status=status.HTTP_404_NOT_FOUND)
        

class NotesCreateView(APIView):
    permission_classes = (IsAuthenticated, )

    @swagger_auto_schema(
        request_body=serializers.NoteCreateSerializer,
        responses={201: serializers.NoteReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(),
                   401:gs.Generic401Serializer()}
    )
    def post(self, request):
        """
        Create New Note
        """
        request_data = request.data.copy()
        request_data['created_by'] = request.user.id
        request_data['modified_by'] = request.user.id
        serializer = serializers.NoteCreateSerializer(data=request_data)
        if serializer.is_valid():
            instance = serializer.save()
            return_serializer = serializers.NoteSerializer(instance)
            return Response({'status': status.HTTP_201_CREATED, 'detail': "Notes Created.", 'data':return_serializer.data}, status=status.HTTP_201_CREATED)
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': serializer.errors, 'data':[]}, status=status.HTTP_400_BAD_REQUEST)


class SingleNoteView(APIView):
    permission_classes = (IsAuthenticated, IsAuthorized)

    @swagger_auto_schema(
        responses={200: serializers.NoteReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request, note_id):
        """
        Get Note By Primary Key. Available Only if Note is Shared with User
        """
        try:
            notes_queryset = Notes.objects.get(pk=note_id, is_active=True, is_deleted=False)
        except Notes.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        
        notes_serializer = serializers.NoteSerializer(notes_queryset)
        return Response({'status': status.HTTP_200_OK, 'detail': 'Note successfully retrieved.', 'metadata':notes_serializer.data})
    