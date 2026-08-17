from unittest.mock import patch

from django.test import SimpleTestCase

from search.context.context_builder import build_context


class ContextBuilderTests(SimpleTestCase):
    """
    Tests for the context builder.
    """

    @patch("search.context.context_builder.calculate_confidence")
    @patch("search.context.context_builder.rerank")
    @patch("search.context.context_builder.retrieve")
    def test_build_context(
        self,
        mock_retrieve,
        mock_rerank,
        mock_confidence,
    ):
        """
        Context builder should assemble
        context, citations and confidence.
        """

        retrieved = [
            {
                "document_id": "DOC-1",
                "source": "pdf",
                "text": "Refresh tokens expire after 30 days.",
                "distance": 0.12,
            },
            {
                "document_id": "DOC-2",
                "source": "jira",
                "text": "Implemented refresh token rotation.",
                "distance": 0.20,
            },
        ]

        mock_retrieve.return_value = retrieved
        mock_rerank.return_value = retrieved
        mock_confidence.return_value = 87

        result = build_context(
            "refresh token"
        )

        self.assertEqual(
            result["confidence"],
            87
        )

        self.assertEqual(
            len(result["citations"]),
            2
        )

        self.assertEqual(
            result["citations"][0]["document_id"],
            "DOC-1"
        )

        self.assertEqual(
            result["citations"][1]["source"],
            "jira"
        )

        self.assertIn(
            "[Source: pdf | Document: DOC-1]",
            result["context"]
        )

        self.assertIn(
            "Refresh tokens expire",
            result["context"]
        )

        self.assertIn(
            "[Source: jira | Document: DOC-2]",
            result["context"]
        )

    @patch("search.context.context_builder.calculate_confidence")
    @patch("search.context.context_builder.rerank")
    @patch("search.context.context_builder.retrieve")
    def test_empty_context(
        self,
        mock_retrieve,
        mock_rerank,
        mock_confidence,
    ):
        """
        Empty retrieval should produce
        an empty context.
        """

        mock_retrieve.return_value = []
        mock_rerank.return_value = []
        mock_confidence.return_value = 0

        result = build_context(
            "unknown topic"
        )

        self.assertEqual(
            result["context"],
            ""
        )

        self.assertEqual(
            result["citations"],
            []
        )

        self.assertEqual(
            result["confidence"],
            0
        )