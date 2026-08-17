import logging

from rank_bm25 import BM25Okapi

from search.models import Chunk

logger = logging.getLogger(__name__)


def bm25_retrieve(
    query,
    source=None,
    k=20,
):
    """
    Retrieves chunks using BM25 keyword search.

    Args:
        query:
            User search query.

        source:
            Optional source filter.
            Examples:
                "jira"
                "slack"
                "meeting"
                "pdf"

        k:
            Number of chunks to return.

    Returns:
        List of chunk dictionaries.
    """

    logger.info(
        "Starting BM25 retrieval for query: %s",
        query,
    )

    # ---------------------------------
    # Load all chunks
    # ---------------------------------

    all_chunks = list(
        Chunk.objects.select_related(
            "document"
        )
    )

    # ---------------------------------
    # Apply Source Filter
    # ---------------------------------

    chunks = []

    for chunk in all_chunks:

        if (
            source is not None
            and chunk.document.source.lower() != source.lower()
        ):
            continue

        chunks.append(chunk)

    if not chunks:

        logger.warning(
            "No matching chunks available."
        )

        return []

    logger.info(
        "Loaded %d chunks.",
        len(chunks),
    )

    # ---------------------------------
    # Tokenize Documents
    # ---------------------------------

    corpus = [
        chunk.text.lower().split()
        for chunk in chunks
    ]

    bm25 = BM25Okapi(
        corpus
    )

    # ---------------------------------
    # Tokenize Query
    # ---------------------------------

    query_tokens = (
        query.lower().split()
    )

    scores = bm25.get_scores(
        query_tokens
    )

    # ---------------------------------
    # Rank Results
    # ---------------------------------

    ranked = sorted(
        zip(scores, chunks),
        key=lambda x: x[0],
        reverse=True,
    )

    results = []

    for score, chunk in ranked[:k]:

        results.append(
            {
                "text": chunk.text,
                "document_id": chunk.document.id,
                "source": chunk.document.source,
                "score": float(score),
                "retrieval_type": "bm25",
            }
        )

    logger.info(
        "Returning %d BM25 results.",
        len(results),
    )

    return results