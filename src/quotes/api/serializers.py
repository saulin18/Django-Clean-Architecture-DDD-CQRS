from rest_framework import serializers


class SubquoteSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    text = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)


class QuoteSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    user_id = serializers.IntegerField()
    text = serializers.CharField(required=True)
    created_at = serializers.DateTimeField(read_only=True)
    updated_at = serializers.DateTimeField(read_only=True)
    subquotes = SubquoteSerializer(many=True)
