from search.knowledge_graph.graph_query import (
    search_graph,
    get_neighbors,
)


def expand_query(query):

    expanded = set()

    matches = search_graph(query)

    for entity in matches:

        expanded.add(entity)

        neighbors = get_neighbors(entity)

        expanded.update(neighbors)

    return list(expanded)