from django.test import SimpleTestCase

from search.knowledge_graph.graph_search import graph_search


class GraphSearchTests(SimpleTestCase):
    def test_graph_search_returns_related_entities(self):
        from search.knowledge_graph.graph_builder import graph

        graph.clear()
        graph.add_node("Neha Joshi", type="person")
        graph.add_node("Backend Alpha", type="project")
        graph.add_node("Kubernetes", type="technology")
        graph.add_edge("Neha Joshi", "Backend Alpha", relation="WORKED_ON")
        graph.add_edge("Backend Alpha", "Kubernetes", relation="USES_TECHNOLOGY")

        result = graph_search("Neha Joshi")

        self.assertIn("Backend Alpha", result)
        self.assertIn("Kubernetes", result)
