from django.test import TestCase

from documents.models import Document

from ingestion.pipeline.ingest_pipeline import run_ingestion


class IngestionPipelineTests(TestCase):
    """
    Integration tests for the ingestion pipeline.
    """

    def test_pipeline_loads_all_documents(self):
        """
        The ingestion pipeline should load every
        document from the datasets.
        """

        count = run_ingestion()

        self.assertEqual(
            count,
            3975
        )

        self.assertEqual(
            Document.objects.count(),
            3975
        )

    def test_running_twice_does_not_create_duplicates(self):
        """
        Running ingestion multiple times should
        update existing documents instead of
        creating duplicates.
        """

        run_ingestion()

        first_count = Document.objects.count()

        run_ingestion()

        second_count = Document.objects.count()

        self.assertEqual(
            first_count,
            second_count
        )

        self.assertEqual(
            second_count,
            3975
        )