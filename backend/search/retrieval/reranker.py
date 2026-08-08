import logging

from search.ranking.ranking_rules import (
    source_bonus,
    freshness_bonus,
)

logger = logging.getLogger(__name__)


def rerank(
    retrieved_chunks,
    max_results=5,
):
    """
    Enterprise reranker.

    Combines:

    - Hybrid retrieval score
    - Source priority
    - Document freshness

    and returns the highest quality chunks.
    """

    logger.info(
        "Starting enterprise reranking."
    )

    reranked = []

    for chunk in retrieved_chunks:

        score = chunk.get(
            "final_score",
            0,
        )

        metadata = chunk.get(
            "metadata",
            {},
        )

        # -----------------------------
        # Source Bonus
        # -----------------------------

        score += source_bonus(
            chunk.get(
                "source"
            )
        )

        # -----------------------------
        # Freshness Bonus
        # -----------------------------

        updated_date = (
            metadata.get("updated_date")
            or metadata.get("created_date")
        )

        score += freshness_bonus(
            updated_date
        )

        chunk["rerank_score"] = score

        reranked.append(chunk)

    reranked.sort(
        key=lambda x: x["rerank_score"],
        reverse=True,
    )

    logger.info(
        "Enterprise reranker selected %d chunks.",
        min(
            len(reranked),
            max_results,
        ),
    )

    return reranked[:max_results]