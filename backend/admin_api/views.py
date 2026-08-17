from rest_framework.views import APIView
from rest_framework.response import Response

from documents.models import Document
from search.models import Chunk
from chatbot.models import ChatSession
from chatbot.models import ChatMessage

from search.knowledge_graph.graph_builder import graph
from admin_api.dashboard.statistics import (
    get_dashboard_statistics,
)
from admin_api.analytics.analytics_service import (
    get_search_analytics,
)

class DocumentStatsAPIView(APIView):

    def get(self, request):

        return Response({

            "total_documents": Document.objects.count(),

            "jira": Document.objects.filter(
                source="jira"
            ).count(),

            "slack": Document.objects.filter(
                source="slack"
            ).count(),

            "meeting": Document.objects.filter(
                source="meeting"
            ).count(),

            "pdf": Document.objects.filter(
                source="pdf"
            ).count(),

        })


class ChunkStatsAPIView(APIView):

    def get(self, request):

        return Response({

            "total_chunks": Chunk.objects.count()

        })


class SessionStatsAPIView(APIView):

    def get(self, request):

        return Response({

            "total_sessions": ChatSession.objects.count(),

            "total_messages": ChatMessage.objects.count(),

        })


class GraphStatsAPIView(APIView):

    def get(self, request):

        return Response({

            "total_nodes": graph.number_of_nodes(),

            "total_edges": graph.number_of_edges(),

        })

class DashboardStatisticsAPIView(APIView):
    """
    Returns enterprise dashboard statistics.
    """

    def get(self, request):

        return Response(
            get_dashboard_statistics()
        )

class SearchAnalyticsAPIView(APIView):
    """
    Returns enterprise search analytics.
    """

    def get(self, request):

        return Response(

            get_search_analytics()

        )