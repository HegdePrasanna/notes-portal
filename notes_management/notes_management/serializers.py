from rest_framework import serializers

class Generic403Serializer(serializers.Serializer):
    detail = serializers.CharField(max_length=50, default="Authentication credentials were not provided.")


class Generic401Serializer(serializers.Serializer):
    detail = serializers.CharField(max_length=50, default="User Not Authorized to Access the Resource.")


class Generic400Serializer(serializers.Serializer):
    status = serializers.IntegerField(default=404)
    detail = serializers.DictField(default={"field_name":["Error Message"]})
    data = serializers.ListField(default=[])


class Generic404Serializer(serializers.Serializer):
    status = serializers.IntegerField(default=404)
    detail = serializers.CharField(max_length=50, default="Requested Resource Not Found.")
    data = serializers.ListField(default=[])