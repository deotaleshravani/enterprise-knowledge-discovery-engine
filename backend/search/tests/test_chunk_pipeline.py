from django.test import TestCase

from documents.models import Document
from search.models import Chunk

from search.chunking.chunk_pipeline import run_chunking


class ChunkPipelineTests(TestCase):
    """
    Tests for the chunking pipeline.
    """

    def setUp(self):
        """
        Create sample documents.
        """

        Document.objects.create(
            id="DOC-001",
            source="pdf",
            text="A " * 3000,
            author="Tester"
        )

        Document.objects.create(
            id="DOC-002",
            source="jira",
            text="B " * 3000,
            author="Tester"
        )

    def test_chunks_are_created(self):
        """
        Running the pipeline should create chunks.
        """

        created = run_chunking()

        self.assertGreater(
            created,
            0
        )

        self.assertGreater(
            Chunk.objects.count(),
            0
        )

    def test_every_chunk_has_document(self):
        """
        Every chunk should belong to a document.
        """

        run_chunking()

        for chunk in Chunk.objects.all():

            self.assertIsNotNone(
                chunk.document
            )

    def test_chunk_indices_are_unique(self):
        """
        A document should not contain duplicate
        chunk indices.
        """

        run_chunking()

        for document in Document.objects.all():

            indices = list(

                Chunk.objects.filter(
                    document=document
                ).values_list(
                    "chunk_index",
                    flat=True
                )

            )

            self.assertEqual(
                len(indices),
                len(set(indices))
            )

    def test_running_twice_does_not_duplicate_chunks(self):
        """
        update_or_create should prevent duplicates.
        """

        run_chunking()

        first = Chunk.objects.count()

        run_chunking()

        second = Chunk.objects.count()

        self.assertEqual(
            first,
            second
        )