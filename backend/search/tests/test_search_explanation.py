from django.test import SimpleTestCase

from search.explanation import explain_search_results


class SearchExplanationTests(SimpleTestCase):
    def test_explain_search_results_uses_metadata_fields(self):
        results = [
            {
                "document_id": "DOC-100",
                "source": "jira",
                "score": 0.92,
                "metadata": {
                    "technology": "Kubernetes",
                    "priority": "Critical",
                    "created_by": "Neha Joshi",
                    "title": "Kubernetes outage resolution",
                },
            },
            {
                "document_id": "DOC-101",
                "source": "slack",
                "score": 0.81,
                "metadata": {
                    "technology": "PostgreSQL",
                    "user": "Amit",
                },
            },
        ]

        explanation = explain_search_results("kubernetes outage", results)

        self.assertIn("matched", explanation)
        self.assertTrue(len(explanation["matched"]) >= 3)
        self.assertIn("Kubernetes", explanation["summary"])
        self.assertEqual(explanation["matched"][0]["field"], "Technology")
        self.assertEqual(explanation["matched"][0]["value"], "Kubernetes")
