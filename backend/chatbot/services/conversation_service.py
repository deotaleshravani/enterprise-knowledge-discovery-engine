import logging

from chatbot.rag_pipeline import ask_ekde

from chatbot.models import ChatSession

from chatbot.session_memory.session_manager import (
    create_session,
    add_message,
    get_history,
)

logger = logging.getLogger(__name__)


def chat(query, session_id=None):
    """
    Handles the complete conversation workflow.

    Steps:
    1. Create or load a chat session.
    2. Retrieve previous conversation history.
    3. Generate an answer using the RAG pipeline.
    4. Save both user and assistant messages.
    5. Return the response.
    """

    logger.info("Starting conversation workflow.")

    # -----------------------------
    # Create or Load Session
    # -----------------------------

    if session_id is None:

        session = create_session(
            title=query[:50]
        )

        logger.info(
            "Created new chat session: %s",
            session.id
        )

    else:

        try:

            session = ChatSession.objects.get(
                id=session_id
            )

            logger.info(
                "Loaded existing session: %s",
                session.id
            )

        except ChatSession.DoesNotExist:

            logger.warning(
                "Session %s not found. Creating a new session.",
                session_id
            )

            session = create_session(
                title=query[:50]
            )

            logger.info(
                "Created replacement session: %s",
                session.id
            )

    # -----------------------------
    # Load Conversation History
    # -----------------------------

    history = get_history(session)

    logger.info(
        "Loaded conversation history (%d characters).",
        len(history)
    )

    # -----------------------------
    # Ask EKDE
    # -----------------------------

    logger.info(
        "Sending query to RAG pipeline."
    )

    response = ask_ekde(
        query=query,
        history=history
    )

    logger.info(
        "Received response from RAG pipeline."
    )

    # -----------------------------
    # Save User Message
    # -----------------------------

    add_message(
        session=session,
        role="user",
        content=query
    )

    logger.info(
        "Saved user message."
    )

    # -----------------------------
    # Save Assistant Message
    # -----------------------------

    add_message(
        session=session,
        role="assistant",
        content=response["answer"]
    )

    logger.info(
        "Saved assistant message."
    )

    # -----------------------------
    # Conversation Complete
    # -----------------------------

    logger.info(
        "Conversation completed successfully."
    )

    return {

        "session_id": session.id,

        "answer": response["answer"],

        "citations": response["citations"],

        "confidence": response["confidence"],

    }