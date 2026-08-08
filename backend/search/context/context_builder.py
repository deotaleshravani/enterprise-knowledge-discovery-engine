import logging

from search.retrieval.hybrid_retriever import hybrid_retrieve
from search.retrieval.reranker import rerank
from chatbot.utils.confidence import calculate_confidence
from search.citations.citation_builder import (
    build_citations,
)

logger = logging.getLogger(__name__)


def build_context(query):
    """
    Builds the context for the LLM.

    Workflow:
    1. Retrieve the top 20 relevant chunks.
    2. Calculate confidence score.
    3. Rerank and remove duplicate chunks.
    4. Build a context string.
    5. Generate citations.
    """

    logger.info(
        "Building context for query: %s",
        query
    )

    # ------------------------------------
    # Retrieve Chunks
    # ------------------------------------

    retrieved = hybrid_retrieve(
        query,
        k=20
    )

    logger.info(
        "Retrieved %d chunks from FAISS.",
        len(retrieved)
    )

    # ------------------------------------
    # Calculate Confidence
    # ------------------------------------

    confidence = calculate_confidence(
        retrieved
    )

    logger.info(
        "Confidence score calculated: %d",
        confidence
    )

    # ------------------------------------
    # Rerank Results
    # ------------------------------------

    chunks = rerank(
        retrieved,
        max_results=5
    )

    logger.info(
        "Reranker selected %d chunks.",
        len(chunks)
    )

    # ------------------------------------
    # Build Context
    # ------------------------------------

    context = ""

    context = ""

    for chunk in chunks:

        context += (
            f"[Source: {chunk['source']} | "
            f"Document: {chunk['document_id']}]\n"
        )

        context += chunk["text"] + "\n\n"

    # ------------------------------------
    # Build Rich Citations
    # ------------------------------------

    citations = build_citations(chunks)

    logger.info(
        "Context built successfully with %d citations.",
        len(citations)
    )

    return {
        "context": context,
        "citations": citations,
        "confidence": confidence
    }