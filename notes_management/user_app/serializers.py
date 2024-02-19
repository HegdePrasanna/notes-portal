from rest_framework import serializers
from .models import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"


class RoleReturnSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=404)
    detail = serializers.CharField(max_length=50, default="Requested Resource Not Found.")
    data = RoleSerializer(many=True)