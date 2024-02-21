from rest_framework import serializers
from django.db.models import Q
from rest_framework.exceptions import NotFound

from user_app.serializers import UserSerializerLite
from .models import Notes, NotesUser, NotesAudit

class NoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notes
        fields = "__all__"

    def create(self, validated_data):
        note_owner = validated_data.get('created_by')
        instance = self.Meta.model(**validated_data)
        instance.save()
        if note_owner:
            _request_data = {
                "user": note_owner,
                "notes": instance,
                "can_read": True,
                "can_edit": True,
                "can_delete": True,
            }
            NotesUser.objects.create(**_request_data)
        return instance


class NoteShareSerializer1(serializers.ModelSerializer):
    user = UserSerializerLite(read_only=True)
    class Meta:
        model = NotesUser
        fields = "__all__"


class NoteSerializer(serializers.ModelSerializer):
    created_by = UserSerializerLite(read_only=True)
    modified_by = UserSerializerLite(read_only=True)
    notes_user = NoteShareSerializer1(read_only=True, many=True)
    class Meta:
        model = Notes
        fields = "__all__"


class NoteShareSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotesUser
        fields = "__all__"

class NoteReturnSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=200)
    detail = serializers.CharField(max_length=50, default="Resource successfully retrieved.")
    data = NoteSerializer(many=True)


class NoteReturnSerializer1(serializers.Serializer):
    status = serializers.IntegerField(default=200)
    detail = serializers.CharField(max_length=50, default="Resource successfully retrieved.")
    data = NoteShareSerializer(many=True)


class NoteShareFormattingSerializer(serializers.Serializer):
    note_shared = NoteShareSerializer1(many=True)
    note_updated = NoteShareSerializer1(many=True)
    validation_errors = serializers.ListField()


class NoteShareReturnSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=200)
    detail = serializers.CharField(max_length=50, default="Resource successfully retrieved.")
    data = NoteShareFormattingSerializer(many=True)


class NotesAuditSerializer(serializers.ModelSerializer):
    modified_by = UserSerializerLite(read_only=True)
    class Meta:
        model = NotesAudit
        fields = "__all__"
    
    def get_total_changes(self, obj):
        total_counts = NotesAudit.objects.filter(notes_id=obj.notes_id, is_active=True, is_deleted=False).count()
        return total_counts


class NotesAuditSerializer1(serializers.Serializer):
    notes = NoteCreateSerializer(read_only=True)
    old_note_content = serializers.CharField(max_length=255)
    new_note_content = serializers.CharField(max_length=255)
    old_note_type = serializers.CharField(max_length=20)
    new_note_type = serializers.CharField(max_length=20)
    created_by = UserSerializerLite(read_only=True)
    modified_by = UserSerializerLite(read_only=True)
    created_at = serializers.DateTimeField()
    modified_at = serializers.DateTimeField()

    def to_representation(self, instance):
        return {'total_changes': 0,
                'changes_history': [{
                    'notes_id': instance.id,
                    'old_note_content': None,
                    'new_note_content': instance.note_content,
                    'old_note_type': None,
                    'new_note_type': instance.note_type,
                    'created_by': UserSerializerLite(instance.created_by).data,
                    'modified_by': UserSerializerLite(instance.created_by).data,
                    'created_at': instance.created_at,
                    'modified_at': instance.modified_at,
                }]
            }


class NotesAuditSerializer2(serializers.Serializer):
    total_changes = serializers.IntegerField()
    changes_history = NotesAuditSerializer(many=True)

class NotesAuditReturnSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=200)
    detail = serializers.CharField(max_length=50, default="Resource successfully retrieved.")
    data = NotesAuditSerializer2()