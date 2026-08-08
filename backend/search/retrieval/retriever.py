import logging

import faiss
import numpy as np

from search.models import Chunk
from search.embeddings.embedding_generator import (
    generate_embedding,
)
from search.vectorstore.faiss_store import (
    load_index,
)

logger = logging.getLogger(__name__)


def retrieve(
    query,
    source=None,
    k=20,
):
    """
    Retrieves the most relevant chunks from FAISS.

    Workflow
    --------
    1. Generate query embedding.
    2. Load FAISS index.
    3. Search top-k vectors.
    4. Load corresponding Chunk objects.
    5. Apply source filtering (optional).
    6. Return formatted results.

    Args
    ----
    query:
        User query.

    source:
        Optional source filter.
        Examples:
            "jira"
            "slack"
            "meeting"
            "pdf"

    k:
        Number of nearest neighbours.

    Returns
    -------
    List of dictionaries.
    """

    logger.info(
        "Starting retrieval for query: %s",
        query,
    )

    # ---------------------------------
    # Load FAISS Index
    # ---------------------------------

    index = load_index()

    logger.info(
        "FAISS index loaded successfully."
    )

    # ---------------------------------
    # Generate Query Embedding
    # ---------------------------------

    query_vector = generate_embedding(query)

    query_vector = np.array(
        [query_vector],
        dtype=np.float32,
    )

    logger.info(
        "Generated query embedding (dimension=%d).",
        query_vector.shape[1],
    )

    # ---------------------------------
    # Search FAISS
    # ---------------------------------

    distances, indices = index.search(
        query_vector,
        k,
    )

    logger.info(
        "FAISS returned %d candidate chunks.",
        len(indices[0]),
    )

    # ---------------------------------
    # Load Chunks
    # ---------------------------------

    chunks = list(
        Chunk.objects.select_related(
            "document"
        ).order_by("id")
    )

    logger.info(
        "Loaded %d chunks from database.",
        len(chunks),
    )

    results = []

    # ---------------------------------
    # Convert FAISS Results
    # ---------------------------------

    for distance, chunk_index in zip(
        distances[0],
        indices[0],
    ):

        if chunk_index >= len(chunks):
            continue

        chunk = chunks[chunk_index]

        # ---------------------------------
        # Source Filtering
        # ---------------------------------

        if (
            source is not None
            and chunk.document.source.lower() != source.lower()
        ):
            continue

        # ---------------------------------
        # Build Result
        # ---------------------------------

        results.append(
            {
                "chunk_id": chunk.id,
                "document_id": chunk.document.id,
                "text": chunk.text,
                "source": chunk.document.source,
                "author": chunk.document.author,
                "date": chunk.document.date,
                "metadata": chunk.document.metadata,
                "distance": float(distance),
                "score": 1.0 / (1.0 + float(distance)),
                "retrieval_type": "faiss",
            }
        )

    logger.info(
        "Retriever returning %d matching chunks.",
        len(results),
    )

    return results