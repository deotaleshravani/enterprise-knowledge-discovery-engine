from rest_framework import serializers
<<<<<<< HEAD
from chatbot.models import ChatSession, ChatMessage
=======
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a


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
<<<<<<< HEAD
    )


class ChatMessageSerializer(serializers.ModelSerializer):
    """
    Serializes individual chat messages within a session.
    """

    class Meta:
        model = ChatMessage
        fields = [
            "id",
            "role",
            "content",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class ChatSessionSerializer(serializers.ModelSerializer):
    """
    Serializes chat session metadata and associated messages.
    """

    messages = ChatMessageSerializer(
        many=True,
        read_only=True
    )

    class Meta:
        model = ChatSession
        fields = [
            "id",
            "title",
            "created_at",
            "updated_at",
            "messages",
        ]
        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]
=======
    )
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
