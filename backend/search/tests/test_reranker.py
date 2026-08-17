from django.test import SimpleTestCase

from search.retrieval.reranker import rerank


class RerankerTests(SimpleTestCase):
    """
    Tests for the reranker.
    """

    def test_remove_duplicate_documents(self):
        """
        Duplicate document IDs should be removed.
        """

        retrieved = [

            {
                "document_id": "DOC-1",
                "source": "pdf",
                "text": "Authentication guide",
                "distance": 0.11,
            },

            {
                "document_id": "DOC-1",
                "source": "pdf",
                "text": "Authentication guide duplicate",
                "distance": 0.12,
            },

            {
                "document_id": "DOC-2",
                "source": "jira",
                "text": "Refresh token bug",
                "distance": 0.20,
            },

            {
                "document_id": "DOC-3",
                "source": "meeting",
                "text": "Deploy patch",
                "distance": 0.30,
            },
        ]

        results = rerank(
            retrieved,
            max_results=5
        )

        self.assertEqual(
            len(results),
            3
        )

        self.assertEqual(
            results[0]["document_id"],
            "DOC-1"
        )

        self.assertEqual(
            results[1]["document_id"],
            "DOC-2"
        )

        self.assertEqual(
            results[2]["document_id"],
            "DOC-3"
        )

    def test_limit_results(self):
        """
        Reranker should return only
        the requested number of chunks.
        """

        retrieved = []

        for i in range(10):

            retrieved.append({

                "document_id": f"DOC-{i}",

                "source": "pdf",

                "text": f"Chunk {i}",

                "distance": float(i)

            })

        results = rerank(
            retrieved,
            max_results=5
        )

        self.assertEqual(
            len(results),
            5
        )

    def test_empty_input(self):
        """
        Empty retrieval should return
        an empty list.
        """

        results = rerank([])

        self.assertEqual(
            results,
            []
        )