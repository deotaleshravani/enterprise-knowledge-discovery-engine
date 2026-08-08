from rest_framework.views import APIView
from rest_framework.response import Response


from search.knowledge_graph.graph_builder import (
    build_graph,
    graph,
)

from search.knowledge_graph.graph_serializer import (
    serialize_graph,
)


from search.knowledge_graph.graph_builder import (
    build_graph,
)

class GraphAPIView(APIView):

    def get(self, request):

        build_graph()

        return Response(
            serialize_graph()
        )

class GraphStatsAPIView(APIView):

    def get(self, request):

        # Rebuild graph from documents
        build_graph()

        return Response({

            "total_nodes": graph.number_of_nodes(),

            "total_edges": graph.number_of_edges(),

        })