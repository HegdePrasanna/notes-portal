from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
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



class Role(AuditModel):
    name = models.CharField(max_length=20, null=False, unique=True,
                            error_messages={"unique": _("A Role with that name already exists."),})
    description = models.TextField(null=True, blank=True)

    @classmethod
    def get_active(self):
        active_objects = Role.objects.filter(is_active=True, is_deleted=False)
        return active_objects



class User(AbstractUser, AuditModel):
    last_login_ip = models.CharField(max_length=30, null=True, blank=True)
    role = models.ForeignKey(Role, on_delete=models.PROTECT, null=True, blank=True, related_name="user_roles")
    # created_at = models.DateTimeField(auto_now_add=True)
    # modified_at = models.DateTimeField(auto_now=True)


    def clean(self):
        super().clean()

        # Check if at least one of role or is_superuser is set
        if not any([self.role, self.is_staff, self.is_superuser]):
            raise ValidationError(_("At least one of role, is_staff, or is_superuser must be set."))

    