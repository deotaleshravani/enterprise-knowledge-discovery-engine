import logging

from documents.models import Document

from search.retrieval.hybrid_retriever import hybrid_retrieve
from search.retrieval.reranker import rerank

from search.formatter.formatter import format_document

from search.citations.citation_builder import (
    build_citation,
)

from chatbot.utils.confidence import calculate_confidence


logger = logging.getLogger(__name__)


def build_context(query):
    """
    Builds structured enterprise context for the LLM.

    Workflow:

    1. Retrieve top 20 relevant chunks.
    2. Calculate confidence.
    3. Rerank the retrieved chunks.
    4. Select the best 5 chunks.
    5. Load the corresponding documents.
    6. Format each document according to its source.
    7. Build source-aware citations.
    8. Return context, citations and confidence.
    """

    logger.info(
        "Building context for query: %s",
        query
    )

    # ==================================================
    # STEP 1 — RETRIEVE
    # ==================================================

    retrieved = hybrid_retrieve(
        query,
        k=20
    )

    logger.info(
        "Retrieved %d chunks.",
        len(retrieved)
    )

    # ==================================================
    # STEP 2 — CONFIDENCE
    # ==================================================

    confidence = calculate_confidence(
        retrieved
    )

    logger.info(
        "Confidence score: %d",
        confidence
    )

    # ==================================================
    # STEP 3 — RERANK
    # ==================================================

    chunks = rerank(
        retrieved,
        max_results=5
    )

    logger.info(
        "Reranker selected %d chunks.",
        len(chunks)
    )

    # ==================================================
    # STEP 4 — BUILD CONTEXT
    # ==================================================

    context_parts = []

    citations = []

    for chunk in chunks:

        document_id = chunk.get(
            "document_id"
        )

        if not document_id:

            logger.warning(
                "Retrieved chunk has no document_id."
            )

            continue

        # ----------------------------------------------
        # Load original document
        # ----------------------------------------------

        try:

            document = Document.objects.get(
                id=document_id
            )

        except Document.DoesNotExist:

            logger.warning(
                "Document %s was not found.",
                document_id
            )

            continue

        # ----------------------------------------------
        # Format according to source
        # ----------------------------------------------

        formatted_document = format_document(
            document
        )

        context_parts.append(
            formatted_document
        )

        # ----------------------------------------------
        # Build source-aware citation
        # ----------------------------------------------

        citation = build_citation(
            document,
            score=chunk.get(
                "final_score",
                0
            )
        )

        citations.append(
            citation
        )

    # ==================================================
    # STEP 5 — JOIN CONTEXT
    # ==================================================

    context = "\n\n".join(
        context_parts
    )

    logger.info(
        "Context built using %d documents.",
        len(context_parts)
    )

    logger.info(
        "Generated %d citations.",
        len(citations)
    )

    # ==================================================
    # RETURN
    # ==================================================

    return {
        "context": context,
        "citations": citations,
        "confidence": confidence,
    }