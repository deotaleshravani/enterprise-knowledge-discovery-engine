from rest_framework import serializers


class DocumentStatsSerializer(serializers.Serializer):

    total_documents = serializers.IntegerField()

    jira = serializers.IntegerField()

    slack = serializers.IntegerField()

    meeting = serializers.IntegerField()

    pdf = serializers.IntegerField()


class ChunkStatsSerializer(serializers.Serializer):

    total_chunks = serializers.IntegerField()


class SessionStatsSerializer(serializers.Serializer):

    total_sessions = serializers.IntegerField()

    total_messages = serializers.IntegerField()


class GraphStatsSerializer(serializers.Serializer):

    total_nodes = serializers.IntegerField()

    total_edges = serializers.IntegerField()