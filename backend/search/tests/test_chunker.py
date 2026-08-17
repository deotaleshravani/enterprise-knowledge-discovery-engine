from django.test import SimpleTestCase

from search.chunking.text_chunker import chunk_text


class TextChunkerTests(SimpleTestCase):
    """
    Unit tests for the chunk_text() function.
    """

    def test_small_text_creates_one_chunk(self):
        """
        Small text should remain a single chunk.
        """

        text = "Hello World"

        chunks = chunk_text(text)

        self.assertEqual(len(chunks), 1)
        self.assertEqual(chunks[0], text)

    def test_empty_text(self):
        """
        Empty text should return an empty list.
        """

        chunks = chunk_text("")

        self.assertEqual(chunks, [])

    def test_large_text_creates_multiple_chunks(self):
        """
        Large text should be split into multiple chunks.
        """

        text = "A " * 3000

        chunks = chunk_text(text)

        self.assertGreater(len(chunks), 1)

    def test_chunk_size_limit(self):
        """
        No chunk should exceed the configured chunk size.
        """

        text = "A " * 3000

        chunks = chunk_text(
            text,
            chunk_size=500,
            chunk_overlap=100
        )

        for chunk in chunks:
            self.assertLessEqual(
                len(chunk),
                500
            )

    def test_chunk_overlap(self):
        """
        Chunking with overlap should produce multiple chunks.
        """

        text = " ".join(
            f"word{i}" for i in range(500)
        )

        chunks = chunk_text(
            text,
            chunk_size=100,
            chunk_overlap=20
        )

        self.assertGreater(
            len(chunks),
            1
        )