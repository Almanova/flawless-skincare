from rest_framework import serializers


class BaseModelSerializer(serializers.Serializer):
    created = serializers.DateTimeField(read_only=True)
    modified = serializers.DateTimeField(read_only=True)
