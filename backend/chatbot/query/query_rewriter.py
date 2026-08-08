import logging

logger = logging.getLogger(__name__)


def rewrite_query(
    query,
    memory,
):
    """
    Rewrites a user query using the
    conversation history stored in
    the database.

    This improves retrieval for
    follow-up questions such as:

        "Who fixed it?"

        "When?"

        "What was the root cause?"

    by attaching previous conversation
    history to the search query.
    """

    logger.info(
        "Rewriting query using conversation history."
    )

    # ----------------------------------
    # No previous history
    # ----------------------------------

    if not memory.strip():

        logger.info(
            "No conversation history found."
        )

        return query

    # ----------------------------------
    # Combine history + current query
    # ----------------------------------

    rewritten_query = (
        f"{memory}\n"
        f"Current Question: {query}"
    )

    logger.info(
        "Rewritten query:\n%s",
        rewritten_query,
    )

    return rewritten_query