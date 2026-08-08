import networkx as nx

from search.knowledge_graph.graph_builder import graph


def degree_ranking():

    return nx.degree_centrality(graph)


def pagerank():

    return nx.pagerank(graph)