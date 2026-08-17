from pathlib import Path

from django.test import TestCase

from documents.models import Document
from search.models import Chunk

from search.embeddings.embedding_pipeline import (
    run_embedding_pipeline,
)

from search.retrieval.retriever import (
    retrieve,
)


TEST_INDEX = (
    Path(__file__).parent /
    "test_vector_store.index"
)


class EmbeddingPipelineTests(TestCase):
    """
    Integration tests for the complete
    embedding pipeline.

    Verifies that:

    Document
        ↓
    Chunk
        ↓
    Embedding
        ↓
    FAISS
        ↓
    Retrieval

    all work together.
    """

    def setUp(self):

        self.document = Document.objects.create(

            id="DOC-001",

            source="pdf",

            text="Authentication uses refresh tokens.",

            metadata={}
        )

        Chunk.objects.create(

            document=self.document,

            chunk_index=0,

            text="Authentication uses refresh tokens."
        )

    def tearDown(self):

        if TEST_INDEX.exists():
            TEST_INDEX.unlink()

    def test_embedding_pipeline_creates_index(self):
        """
        Running the embedding pipeline
        should create a FAISS index.
        """

        count = run_embedding_pipeline(
            index_path=TEST_INDEX
        )

        self.assertEqual(count, 1)

        self.assertTrue(
            TEST_INDEX.exists()
        )

    def test_retrieve_returns_expected_chunk(self):
        """
        Retrieval should return the
        authentication chunk.
        """

        run_embedding_pipeline(
            index_path=TEST_INDEX
        )

        results = retrieve(
            "authentication",
            index_path=TEST_INDEX
        )

        self.assertEqual(
            len(results),
            1
        )

        self.assertEqual(
            results[0]["document_id"],
            "DOC-001"
        )

        self.assertIn(
            "Authentication",
            results[0]["text"]
        )