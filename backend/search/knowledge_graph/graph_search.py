<<<<<<< HEAD
from search.knowledge_graph.graph_builder import graph


def graph_search(query):
    """
    Expand a query against the enterprise graph.

    The function returns the matched entity plus all neighboring entities,
    which supports questions like:
    - Who worked with Neha?
    - Which projects use PostgreSQL?
    - Which team handles Kubernetes?
    """
    if not query:
        return []

    q = str(query).strip().lower()
    if not q:
        return []

    exact_matches = [
        node for node in graph.nodes
        if str(node).lower() == q
    ]

    if exact_matches:
        root = exact_matches[0]
        expanded = {root}
        expanded.update(graph.neighbors(root))
        for neighbor in list(graph.neighbors(root)):
            expanded.update(graph.neighbors(neighbor))
        return sorted(str(item) for item in expanded)

    matches = []
    for node in graph.nodes:
        node_text = str(node).lower()
        if q in node_text:
            matches.append(str(node))

    expanded = set(matches)
    for node_name in list(matches):
        if node_name in graph:
            expanded.update(str(neighbor) for neighbor in graph.neighbors(node_name))

    return sorted(expanded)
=======
from search.knowledge_graph.graph_expander import (
    expand_query,
)


def graph_search(query):

    return expand_query(query)
>>>>>>> 295313f9544a55975afdff91c3cab55d8a5a635a
