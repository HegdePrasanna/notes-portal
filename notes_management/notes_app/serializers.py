from rest_framework import serializers
from .models import Notes, NotesUser
from django.db.models import Q
from rest_framework.exceptions import NotFound
from user_app.serializers import UserSerializerLite

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


class NoteSerializer(serializers.ModelSerializer):
    created_by = UserSerializerLite(read_only=True)
    modified_by = UserSerializerLite(read_only=True)
    class Meta:
        model = Notes
        fields = "__all__"
    
    



class NoteReturnSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=200)
    detail = serializers.CharField(max_length=50, default="Resource successfully retrieved.")
    data = NoteSerializer(many=True)