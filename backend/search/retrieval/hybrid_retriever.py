import logging
from search.filters.metadata_filter import (
    apply_filters,
)

from search.intent.detector import detect_intent
from search.retrieval.metadata_booster import boost_results
from search.retrieval.diversify import diversify_results
from chatbot.query.query_rewriter import (
    rewrite_query,
)
from search.knowledge_graph.graph_query import (
    search_graph,
)
from search.retrieval.bm25_retriever import (
    bm25_retrieve,
)

from search.retrieval.retriever import (
    retrieve,
)

from search.query_expansion.query_expander import (
    expand_query,
)

from search.source_detection.detector import (
    detect_source,
)
from search.optimizer.context_optimizer import (
    optimize_context,
)
logger = logging.getLogger(__name__)


def normalize_scores(results, score_key):
    """
    Normalizes scores into the range [0, 1].

    This allows FAISS and BM25 scores
    to be combined fairly.
    """

    if not results:
        return results

    scores = [
        result[score_key]
        for result in results
    ]

    minimum = min(scores)
    maximum = max(scores)

    if minimum == maximum:

        for result in results:
            result["normalized_score"] = 1.0

        return results

    for result in results:

        result["normalized_score"] = (
            (result[score_key] - minimum)
            /
            (maximum - minimum)
        )

    return results


def hybrid_retrieve(
    query,
    memory=None,
    k=20,
    semantic_weight=0.7,
    keyword_weight=0.3,
):
    """
    Enterprise Hybrid Retrieval Pipeline

    User Query
          ↓
    Intent Detection
          ↓
    Source Detection
          ↓
    Query Rewriter (optional)
          ↓
    Query Expansion
          ↓
    FAISS Retrieval
          ↓
    BM25 Retrieval
          ↓
    Score Normalization
          ↓
    Weighted Score Fusion
          ↓
    Metadata Boosting
          ↓
    Sort
          ↓
    Top K Results
    """

    logger.info(
        "Starting hybrid retrieval."
    )

    # ----------------------------------
    # Intent Detection
    # ----------------------------------

    intent = detect_intent(query)
    graph_results = search_graph(query)
    query = expand_query(query)
    logger.info(
        "Knowledge Graph expanded query: %s",
        query,
    )
    logger.info(
        "Knowledge Graph returned %d related entities.",
        len(graph_results),
    )

    if graph_results:

        for item in graph_results:

            query += " " + item["entity"]

    logger.info(
        "Detected intent: %s",
        intent
    )

    # ----------------------------------
    # Source Detection
    # ----------------------------------

    source = detect_source(query)

    logger.info(
        "Detected source: %s",
        source,
    )

    # ----------------------------------
    # Rewrite Query (Conversation Aware)
    # ----------------------------------

    if memory is not None:

        logger.info(
            "Conversation memory detected."
        )

        query = rewrite_query(
            query,
            memory,
        )

        logger.info(
            "Rewritten query: %s",
            query,
        )

    # ----------------------------------
    # Query Expansion
    # ----------------------------------

    query = expand_query(query)

    logger.info(
        "Expanded into %d queries.",
        len(query),
    )

    query = " ".join(query)

    logger.info(
        "Expanded query: %s",
        query,
    )

    # ----------------------------------
    # Semantic Retrieval (FAISS)
    # ----------------------------------

    semantic_results = retrieve(
        query=query,
        source=source,
        k=k,
    )

    logger.info(
        "FAISS returned %d results.",
        len(semantic_results),
    )

    # Convert FAISS distance into similarity

    for result in semantic_results:

        similarity = (
            1
            /
            (1 + result["distance"])
        )

        result["score"] = similarity

    normalize_scores(
        semantic_results,
        "score",
    )

    # ----------------------------------
    # Keyword Retrieval (BM25)
    # ----------------------------------

    keyword_results = bm25_retrieve(
        query=query,
        source=source,
        k=k,
    )

    logger.info(
        "BM25 returned %d results.",
        len(keyword_results),
    )

    normalize_scores(
        keyword_results,
        "score",
    )

    # ----------------------------------
    # Merge Results
    # ----------------------------------

    merged = {}

    # Add semantic results

    for result in semantic_results:

        key = (
            result["document_id"],
            result["chunk_id"],
        )

        merged[key] = result.copy()

        merged[key]["final_score"] = (
            semantic_weight
            *
            result["normalized_score"]
        )

    # Merge keyword results

    for result in keyword_results:

        key = (
            result["document_id"],
            result.get(
                "chunk_id",
                -1,
            ),
        )

        if key in merged:

            merged[key]["final_score"] += (
                keyword_weight
                *
                result["normalized_score"]
            )

        else:

            merged[key] = result.copy()

            merged[key]["final_score"] = (
                keyword_weight
                *
                result["normalized_score"]
            )

    # ----------------------------------
    # Sort
    # ----------------------------------

    final_results = sorted(
        merged.values(),
        key=lambda x: x["final_score"],
        reverse=True,
    )

    # ----------------------------------
    # Metadata Boosting
    # ----------------------------------

    final_results = boost_results(
        final_results,
        intent,
    )
    final_results = diversify_results(
        final_results,
        k=k,
    )
    final_results = optimize_context(
        final_results,
    )

    final_results = apply_filters(
        final_results,
        query,
    )

    logger.info(
        "Hybrid retrieval returning %d results.",
        min(
            len(final_results),
            k,
        ),
    )

    return final_results[:k]