from rest_framework import serializers
from .models import Role, User
from django.db.models import Q
from rest_framework.exceptions import NotFound


class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = "__all__"
    
    def create(self, validated_data):
        # is_deleted is a soft delete field.
        omitted_field = validated_data.pop('is_deleted', None)
        role = Role.objects.create(**validated_data)
        return role

    def update(self, instance, validated_data):
        omitted_field = validated_data.pop('is_deleted', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class RoleReturnSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=200)
    detail = serializers.CharField(max_length=50, default="Resource successfully retrieved.")
    data = RoleSerializer(many=True)


class UserSerializerCreate(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "password", "role")
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', 'Welcome@123')
        
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        
        instance.save()
        return instance

    def update(self, instance, validated_data):
        omitted_field = validated_data.pop('is_deleted', None)
        password = validated_data.pop('password')
        
        if password is not None:
            instance.set_password(password)
        
        for key, value in validated_data.items():
            setattr(instance, key, value)
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    role = RoleSerializer(read_only=True)
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {'password': {'write_only': True}}
    
    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('role')
        return queryset


class UserReturnSerializer(serializers.Serializer):
    status = serializers.IntegerField(default=200)
    detail = serializers.CharField(max_length=50, default="Resource successfully retrieved.")
    data = UserSerializer(many=True)