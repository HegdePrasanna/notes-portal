from django.db import models
from user_app.models import User
# Create your models here.

class AuditModel(models.Model):
    """
    This is just audit model
    """
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    
    class Meta:
        abstract = True


class Notes(AuditModel):
    note_content = models.TextField()
    note_type = models.CharField(max_length=20, default="text")
    users = models.ManyToManyField(User, through='NotesUser', related_name='notes')
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_creator')
    modified_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='note_modifier')


    @classmethod
    def get_active(self):
        active_objects = Notes.objects.filter(is_active=True, is_deleted=False)
        return active_objects


class NotesUser(AuditModel):
    notes = models.ForeignKey(Notes, on_delete=models.CASCADE, related_name='notes_user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_notes')
    can_read = models.BooleanField(default=True)
    can_edit = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)