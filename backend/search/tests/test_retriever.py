from unittest.mock import Mock, patch

from django.test import TestCase

from documents.models import Document
from search.models import Chunk

from search.retrieval.retriever import retrieve


class RetrieverTests(TestCase):
    """
    Tests for the semantic retriever.
    """

    def setUp(self):
        """
        Create sample chunks.
        """

        document = Document.objects.create(
            id="DOC-001",
            source="pdf",
            text="Enterprise authentication guide",
            author="Admin",
        )

        Chunk.objects.create(
            document=document,
            chunk_index=0,
            text="Refresh tokens are valid for 30 days."
        )

        Chunk.objects.create(
            document=document,
            chunk_index=1,
            text="JWT tokens expire after one hour."
        )

    @patch(
        "search.retrieval.retriever.generate_embedding"
    )
    @patch(
        "search.retrieval.retriever.load_index"
    )
    def test_retrieve(
        self,
        mock_load_index,
        mock_generate_embedding
    ):
        """
        Retriever should return
        matching chunks.
        """

        mock_generate_embedding.return_value = [0.1] * 384

        fake_index = Mock()

        fake_index.search.return_value = (

            [[0.12, 0.25]],

            [[0, 1]]

        )

        mock_load_index.return_value = fake_index

        results = retrieve(
            "refresh token"
        )

        self.assertEqual(
            len(results),
            2
        )

        self.assertEqual(
            results[0]["document_id"],
            "DOC-001"
        )

        self.assertEqual(
            results[0]["source"],
            "pdf"
        )

        self.assertIn(
            "Refresh tokens",
            results[0]["text"]
        )

        self.assertEqual(
            results[0]["distance"],
            0.12
        )

    @patch(
        "search.retrieval.retriever.generate_embedding"
    )
    @patch(
        "search.retrieval.retriever.load_index"
    )
    def test_empty_results(
        self,
        mock_load_index,
        mock_generate_embedding
    ):
        """
        Retriever should return
        an empty list when FAISS
        finds nothing.
        """

        mock_generate_embedding.return_value = [0.1] * 384

        fake_index = Mock()

        fake_index.search.return_value = (

            [[]],

            [[-1]]

        )

        mock_load_index.return_value = fake_index

        results = retrieve(
            "nonexistent topic"
        )

        self.assertEqual(
            results,
            []
        )