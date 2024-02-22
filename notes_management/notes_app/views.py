from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotFound, NotAuthenticated
from rest_framework import status
from drf_yasg.utils import swagger_auto_schema
from .models import Notes, NotesUser, NotesAudit
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


class IsAuthorizedToShare(BasePermission):
    """
    Custom permission to only check authorization. Users can share notes only if they have write access to it
    """
    def has_permission(self, request, view):
        """
        Check if the user making the request is authorized.
        """
        req_data = request.data.copy()
        can_share = False
        for i in req_data:
            try:
                note_exist = Notes.objects.get(pk=i.get('notes'), is_active=True, is_deleted=False)
            except Notes.DoesNotExist:
                raise NotFound("Requested Note Not Present.!")
            # is_owner = note_exist.created_by
            if note_exist.created_by != request.user:
                raise PermissionDenied("Only Owner Can Share the Note.!")
            can_share = True
        return can_share
    

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
        responses={200: serializers.NoteReturnSerializer1(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request, note_id):
        """
        Get Note By Primary Key. Available Only if Note is Shared with User
        """
        try:
            notes_queryset = Notes.objects.get(pk=note_id, is_active=True, is_deleted=False)
        except Notes.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        
        notes_serializer = serializers.NoteCreateSerializer(notes_queryset)
        return Response({'status': status.HTTP_200_OK, 'detail': 'Note successfully retrieved.', 'metadata':notes_serializer.data})

    @swagger_auto_schema(
        request_body=serializers.NoteCreateSerializer,
        responses={201: serializers.NoteReturnSerializer(), 400:gs.Generic400Serializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer(),
                   401:gs.Generic401Serializer()}
    )
    def put(self, request, note_id):
        """
        Update Note By Primary Key. Available Only if Note is Shared with User and User can edit permission
        """
        try:
            notes_queryset = Notes.objects.get(pk=note_id, is_active=True, is_deleted=False)
        except Notes.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        
        request_data = request.data.copy()
        request_data['modified_by'] = request.user.id
        serializer = serializers.NoteCreateSerializer(notes_queryset, data=request_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_200_OK, 'detail': 'Note successfully updated.', 'metadata':serializer.data})
        return Response({'status': status.HTTP_400_BAD_REQUEST, 'detail': 'Unable to update Note.', 'metadata':serializer.errors})
    

class SingleNoteDetailView(APIView):
    permission_classes = (IsAuthenticated, IsAuthorized)

    @swagger_auto_schema(
        responses={200: serializers.NoteReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request, note_id):
        """
        Get Note By Primary Key. Available Only if Note is Shared with User. Includes details of shared users and owner information
        """
        try:
            notes_queryset = Notes.objects.get(pk=note_id, is_active=True, is_deleted=False)
        except Notes.DoesNotExist:
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
        
        notes_serializer = serializers.NoteSerializer(notes_queryset)
        return Response({'status': status.HTTP_200_OK, 'detail': 'Note successfully retrieved.', 'metadata':notes_serializer.data})


class NotesShareView(APIView):
    permission_classes = (IsAuthenticated, IsAuthorizedToShare)

    @swagger_auto_schema(
        request_body=serializers.NoteShareSerializer(many=True), 
        responses={200: serializers.NoteShareReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def post(self, request):
        """
        Share Notes with Other users. If already shared then Update the details with new input
        """
        request_data = request.data.copy()
        new_note_shared = []
        note_perm_updated = []
        errors_in_data = []
        for data in request_data:
            user_id = data.get('user')
            notes_id = data.get('notes')

            try:
                shared_note = NotesUser.objects.get(user_id=user_id, notes_id=notes_id)
                data['modified_by'] = request.user
                serializer = serializers.NoteShareSerializer(shared_note, data=data, partial=True)
                if serializer.is_valid():
                    instance = serializer.save()
                    note_perm_updated.append(instance)
                else:
                    errors_in_data.append(serializer.errors)
            except NotesUser.DoesNotExist:
                data['created_by'] = request.user
                data['modified_by'] = request.user
                serializer = serializers.NoteShareSerializer(data=data)
                if serializer.is_valid():
                    instance = serializer.save()
                    new_note_shared.append(instance)
                else:
                    errors_in_data.append(serializer.errors)
        return_data = {
            'note_shared': serializers.NoteShareSerializer1(new_note_shared, many=True).data,
            'note_updated': serializers.NoteShareSerializer1(note_perm_updated, many=True).data,
            'validation_errors': errors_in_data
            }
        return Response({'status': status.HTTP_200_OK, 'detail': "Notes Share Completed.", 'data':return_data}, status=status.HTTP_200_OK)



class NotesHistoryView(APIView):
    permission_classes = (IsAuthenticated, IsAuthorized)

    @swagger_auto_schema(
        responses={200: serializers.NotesAuditReturnSerializer(), 403:gs.Generic403Serializer(), 404:gs.Generic404Serializer()}
    )
    def get(self, request, note_id):
        """
        Get Note By Primary Key. Available Only if Note is Shared with User. Includes details of shared users and owner information
        """
        
        notes_history_queryset = NotesAudit.objects.filter(notes_id=note_id, is_active=True, is_deleted=False)
        if not notes_history_queryset.exists():
            try:
                note_exist = Notes.objects.get(pk=note_id, is_active=True, is_deleted=False)
            except NotesAudit.DoesNotExist:
                return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Note Not Found.', 'metadata':[]}, status=status.HTTP_404_NOT_FOUND)
            serializer = serializers.NotesAuditSerializer1(note_exist)
            return Response({'status': status.HTTP_404_NOT_FOUND, 'detail': 'Requested Note Does Not Have Any Modifications Found.', 'metadata':serializer.data}, status=status.HTTP_404_NOT_FOUND)
        total_changes = notes_history_queryset.count()
        notes_audit_serializer = serializers.NotesAuditSerializer(notes_history_queryset, many=True)
        return_data = {
            'total_changes': total_changes,
            'changes_history': notes_audit_serializer.data
        }
        return Response({'status': status.HTTP_200_OK, 'detail': 'Note History successfully retrieved.', 'metadata':return_data})
