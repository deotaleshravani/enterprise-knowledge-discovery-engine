from collections import Counter

from documents.models import Document
from search.models import Chunk

from chatbot.models import (
    ChatSession,
    ChatMessage,
)
from search.knowledge_graph.graph_builder import (
    build_graph,
    graph,
)
# from search.knowledge_graph.graph_builder import graph


def get_dashboard_statistics():
    """
    Returns dashboard statistics for the
    Enterprise Knowledge Dashboard.
    """
    build_graph()

    source_counter = Counter(
        Document.objects.values_list(
            "source",
            flat=True,
        )
    )

    return {

        "documents": Document.objects.count(),

        "chunks": Chunk.objects.count(),

        "graph_nodes": graph.number_of_nodes(),

        "graph_edges": graph.number_of_edges(),

        "chat_sessions": ChatSession.objects.count(),

        "chat_messages": ChatMessage.objects.count(),

        "documents_by_source": dict(source_counter),
    }