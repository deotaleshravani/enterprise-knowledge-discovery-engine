from django.test import TestCase

from documents.models import Document
from search.models import Chunk

from search.chunking.chunk_pipeline import run_chunking
from search.embeddings.embedding_pipeline import (
    run_embedding_pipeline,
)
from search.retrieval.retriever import retrieve


class SearchPipelineIntegrationTests(TestCase):
    """
    End-to-end integration test for the search pipeline.

    Workflow:
    Document
        ↓
    Chunking
        ↓
    Embeddings
        ↓
    FAISS
        ↓
    Retrieval
    """

    def test_complete_search_pipeline(self):
        """
        A stored document should be retrievable
        after chunking and embedding.
        """

        Document.objects.create(
            id="DOC-001",
            source="pdf",
            text=(
                "Python is a popular programming language "
                "used for artificial intelligence."
            )
        )

        run_chunking()

        self.assertEqual(
            Chunk.objects.count(),
            1
        )

        run_embedding_pipeline()

        results = retrieve(
            "What is Python?",
            k=5
        )

        self.assertGreater(
            len(results),
            0
        )

        self.assertEqual(
            results[0]["document_id"],
            "DOC-001"
        )

        self.assertIn(
            "Python",
            results[0]["text"]
        )