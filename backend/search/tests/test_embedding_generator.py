from django.test import SimpleTestCase

from search.embeddings.embedding_generator import (
    generate_embedding
)


class EmbeddingGeneratorTests(SimpleTestCase):
    """
    Unit tests for the embedding generator.
    """

    def test_returns_list(self):
        """
        Embedding should be returned as a Python list.
        """

        embedding = generate_embedding(
            "Hello World"
        )

        self.assertIsInstance(
            embedding,
            list
        )

    def test_embedding_not_empty(self):
        """
        Embedding should contain values.
        """

        embedding = generate_embedding(
            "Hello World"
        )

        self.assertGreater(
            len(embedding),
            0
        )

    def test_embedding_dimension(self):
        """
        BGE Small produces 384-dimensional embeddings.
        """

        embedding = generate_embedding(
            "Hello World"
        )

        self.assertEqual(
            len(embedding),
            384
        )

    def test_same_text_same_embedding(self):
        """
        Same text should always produce
        the same embedding.
        """

        emb1 = generate_embedding(
            "Enterprise AI"
        )

        emb2 = generate_embedding(
            "Enterprise AI"
        )

        self.assertEqual(
            emb1,
            emb2
        )

    def test_different_texts(self):
        """
        Different text should produce
        different embeddings.
        """

        emb1 = generate_embedding(
            "Enterprise AI"
        )

        emb2 = generate_embedding(
            "Football Match"
        )

        self.assertNotEqual(
            emb1,
            emb2
        )

    def test_empty_string(self):
        """
        Empty string should still
        return a valid embedding.
        """

        embedding = generate_embedding("")

        self.assertEqual(
            len(embedding),
            384
        )

    def test_unicode_text(self):
        """
        Unicode text should work correctly.
        """

        embedding = generate_embedding(
            "नमस्ते दुनिया"
        )

        self.assertEqual(
            len(embedding),
            384
        )