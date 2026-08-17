<<<<<<< HEAD
import csv
import io

from django.http import HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response

from search.explanation import explain_search_results
=======
from rest_framework.views import APIView
from rest_framework.response import Response


>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
from search.knowledge_graph.graph_builder import (
    build_graph,
    graph,
)
<<<<<<< HEAD
from search.knowledge_graph.graph_search import graph_search
from search.knowledge_graph.graph_serializer import (
    serialize_graph,
)
from search.models import SearchAnalytics
from search.retrieval.hybrid_retriever import hybrid_retrieve


class SearchExplanationAPIView(APIView):
    """Explain how the retrieval matched the user's query."""

    def get(self, request):
        query = request.query_params.get("q") or request.query_params.get("query") or ""
        if not query:
            return Response({"summary": "No search query provided.", "matched": []})

        results = hybrid_retrieve(query, k=10)
        explanation = explain_search_results(query, results)
        return Response(explanation)


class GraphSearchAPIView(APIView):
    """Graph-based relationship lookup for enterprise entities."""

    def get(self, request):
        query = request.query_params.get("q") or request.query_params.get("query") or ""
        build_graph()
        if not query:
            return Response({"query": query, "results": []})

        return Response({"query": query, "results": graph_search(query)})


class ExportAPIView(APIView):
    """Download enterprise analytics data as JSON or CSV."""

    def get(self, request, file_format):
        records = list(SearchAnalytics.objects.order_by("-created_at").values())

        if file_format == "json":
            return Response(records)

        if file_format == "csv":
            output = io.StringIO()
            fieldnames = [
                "id", "query", "intent", "source", "confidence",
                "retrieved_chunks", "response_time", "created_at",
            ]
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for row in records:
                writer.writerow(row)

            response = HttpResponse(output.getvalue(), content_type="text/csv")
            response["Content-Disposition"] = "attachment; filename=ekde_export.csv"
            return response

        return Response({"error": "Unsupported export format."}, status=400)

=======

from search.knowledge_graph.graph_serializer import (
    serialize_graph,
)


from search.knowledge_graph.graph_builder import (
    build_graph,
)
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a

class GraphAPIView(APIView):

    def get(self, request):

        build_graph()

        return Response(
            serialize_graph()
        )

<<<<<<< HEAD

=======
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
class GraphStatsAPIView(APIView):

    def get(self, request):

<<<<<<< HEAD
        build_graph()

        return Response({
            "total_nodes": graph.number_of_nodes(),
            "total_edges": graph.number_of_edges(),
=======
        # Rebuild graph from documents
        build_graph()

        return Response({

            "total_nodes": graph.number_of_nodes(),

            "total_edges": graph.number_of_edges(),

>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
        })