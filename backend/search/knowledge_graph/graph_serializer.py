from search.knowledge_graph.graph_builder import graph


def serialize_graph():

    nodes = []

    edges = []

    for node, attributes in graph.nodes(data=True):

        nodes.append({
            "id": node,
            "type": attributes.get("type", "entity")
        })

    for source, target, attributes in graph.edges(data=True):

        edges.append({
            "source": source,
            "target": target,
            "relation": attributes.get("relation", "")
        })

    return {
        "nodes": nodes,
        "edges": edges,
    }