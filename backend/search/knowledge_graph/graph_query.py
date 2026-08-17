from search.knowledge_graph.graph_builder import graph


def get_neighbors(entity):

    if entity not in graph:
        return []

    return list(graph.neighbors(entity))


def get_relations(entity):

    if entity not in graph:
        return []

    relations = []

    for neighbor in graph.neighbors(entity):

        relation = graph.edges[
            entity,
            neighbor
        ]["relation"]

        relations.append({

            "entity": neighbor,

            "relation": relation,

        })

    return relations


def search_graph(query):
    """
    Search graph nodes whose names
    match the user's query.

    Returns:

        List[str]
    """

    query = query.lower()

    matches = []

    for node in graph.nodes():

        if query in str(node).lower():

            matches.append(node)

    return matches