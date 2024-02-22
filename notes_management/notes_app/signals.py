from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Notes, NotesAudit


@receiver(pre_save, sender=Notes)
def track_note_changes(sender, instance, **kwargs):
    try:
        old_instance = Notes.objects.get(pk=instance.pk)
    except Notes.DoesNotExist:
        # This is empty because does not exist. We have to create one
        return None

    if old_instance.note_content != instance.note_content or old_instance.note_type != instance.note_type:
        audit_log = NotesAudit(
            notes=instance,
            modified_by=instance.modified_by,
            old_note_content=old_instance.note_content,
            new_note_content=instance.note_content,
            old_note_type=old_instance.note_type,
            new_note_type=instance.note_type,
            created_at=instance.created_at
        )
        audit_log.save()