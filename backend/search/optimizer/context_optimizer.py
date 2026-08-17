import logging

logger = logging.getLogger(__name__)


def optimize_context(
    results,
    max_chunks_per_document=2,
    max_chunks_per_source=5,
):
    """
    Optimizes retrieved context before it is
    sent to the LLM.

    Optimizations

    1. Remove duplicate chunks

    2. Limit chunks per document

    3. Balance sources
    """

    logger.info(
        "Starting context optimization."
    )

    optimized = []

    seen_chunks = set()

    document_counts = {}

    source_counts = {}

    for result in results:

        text = result["text"].strip()

        # -----------------------------
        # Remove duplicate chunks
        # -----------------------------

        if text in seen_chunks:
            continue

        seen_chunks.add(text)

        # -----------------------------
        # Limit chunks per document
        # -----------------------------

        document_id = result["document_id"]

        document_count = document_counts.get(
            document_id,
            0,
        )

        if document_count >= max_chunks_per_document:
            continue

        # -----------------------------
        # Limit chunks per source
        # -----------------------------

        source = result["source"]

        source_count = source_counts.get(
            source,
            0,
        )

        if source_count >= max_chunks_per_source:
            continue

        document_counts[document_id] = (
            document_count + 1
        )

        source_counts[source] = (
            source_count + 1
        )

        optimized.append(result)

    logger.info(
        "Context optimization reduced %d chunks to %d.",
        len(results),
        len(optimized),
    )

    logger.info(
        "Source distribution: %s",
        source_counts,
    )

    return optimized