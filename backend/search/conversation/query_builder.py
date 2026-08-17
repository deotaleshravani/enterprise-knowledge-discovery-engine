import logging

logger = logging.getLogger(__name__)


def build_query(
    question,
    history=None,
    max_history=3,
):
    """
    Builds a richer search query by
    combining recent conversation history
    with the current user question.
    """

    if not history:
        logger.info(
            "No conversation history."
        )
        return question

    recent = history[-max_history:]

    previous_questions = []

    for item in recent:

        if item.get("role") == "user":

            previous_questions.append(
                item["content"]
            )

    full_query = " ".join(
        previous_questions + [question]
    )

    logger.info(
        "Conversation query built."
    )

    return full_query