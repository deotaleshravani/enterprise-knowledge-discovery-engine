from rest_framework import serializers


class ChatRequestSerializer(serializers.Serializer):
    """
    Validates incoming chat requests.
    """

    question = serializers.CharField(
        max_length=2000
    )

    session_id = serializers.UUIDField(
        required=False,
        allow_null=True
    )


class ChatResponseSerializer(serializers.Serializer):
    """
    Formats chatbot responses.
    """

    answer = serializers.CharField()

    confidence = serializers.IntegerField()

    # Source-aware citations (dynamic structure)
    citations = serializers.JSONField()

    session_id = serializers.UUIDField(
        required=False,
        allow_null=True
    )