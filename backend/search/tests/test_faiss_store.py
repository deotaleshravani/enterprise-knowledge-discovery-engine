import os

import numpy as np
from django.test import SimpleTestCase

from search.vectorstore.faiss_store import (
    save_index,
    load_index,
    INDEX_PATH,
)


class FaissStoreTests(SimpleTestCase):
    """
    Tests for the FAISS vector store.
    """

    def setUp(self):
        """
        Ensure every test starts with
        no FAISS index.
        """

        if INDEX_PATH.exists():
            os.remove(INDEX_PATH)

    def tearDown(self):
        """
        Remove the FAISS index after
        every test.
        """

        if INDEX_PATH.exists():
            os.remove(INDEX_PATH)

    def test_save_and_load_index(self):
        """
        Saving an index should create
        a FAISS file that can be
        loaded again.
        """

        embeddings = np.array(
            [
                [0.1] * 384,
                [0.2] * 384,
                [0.3] * 384,
            ],
            dtype=np.float32,
        )

        save_index(embeddings)

        self.assertTrue(
            INDEX_PATH.exists()
        )

        index = load_index()

        self.assertEqual(
            index.ntotal,
            3
        )

        self.assertEqual(
            index.d,
            384
        )

    def test_empty_embeddings(self):
        """
        Saving an empty embedding list
        should not create an index.
        """

        save_index([])

        self.assertFalse(
            INDEX_PATH.exists()
        )