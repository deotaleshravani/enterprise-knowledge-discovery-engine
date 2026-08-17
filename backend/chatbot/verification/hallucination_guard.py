import logging

logger = logging.getLogger(__name__)


def verify_answer(
    answer,
    context,
    confidence,
):
    """
    Performs a lightweight verification of
    the LLM answer against the retrieved context.

    If the answer appears unsupported,
    confidence is reduced and a safer
    response may be returned.
    """

    logger.info(
        "Running hallucination guard."
    )

    answer_lower = answer.lower()
    context_lower = context.lower()

    # -------------------------------
    # Empty answer
    # -------------------------------

    if not answer.strip():

        logger.warning(
            "Empty answer generated."
        )

        return {
            "answer": (
                "I couldn't generate an answer."
            ),
            "confidence": 0,
        }

    # -------------------------------
    # Very low retrieval confidence
    # -------------------------------

    if confidence < 30:

        logger.warning(
            "Low retrieval confidence."
        )

        return {
            "answer": (
                "I couldn't find sufficient evidence "
                "in the Enterprise Knowledge Base "
                "to answer this question."
            ),
            "confidence": confidence,
        }

    # -------------------------------
    # Basic evidence check
    # -------------------------------

    supported_words = 0

    words = answer_lower.split()

    for word in words:

        if len(word) < 5:
            continue

        if word in context_lower:
            supported_words += 1

    logger.info(
        "Supported words: %d",
        supported_words,
    )

    # -------------------------------
    # Unsupported answer
    # -------------------------------

    if supported_words < 5:

        logger.warning(
            "Answer appears weakly supported."
        )

        confidence = max(
            confidence - 30,
            10
        )

    return {
        "answer": answer,
        "confidence": confidence,
    }