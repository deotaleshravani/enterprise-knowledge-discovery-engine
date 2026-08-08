import logging

from chatbot.models import ChatSession

from chatbot.session_memory.session_manager import (
    create_session,
    add_message,
    get_history,
)

from chatbot.query.query_rewriter import rewrite_query
from chatbot.rag_pipeline import ask_ekde

from chatbot.verification.hallucination_guard import (
    verify_answer,
)
from search.analytics.metrics import (
    Timer,
    log_search,
)

from search.intent.detector import (
    detect_intent,
)

from search.source_detection.detector import (
    detect_source,
)

logger = logging.getLogger(__name__)


class ChatPipeline:
    """
    Enterprise Chat Pipeline

    Workflow
    --------
    User Question
            ↓
    Load/Create Session
            ↓
    Save User Message
            ↓
    Load Conversation History
            ↓
    Rewrite Query
            ↓
    RAG Pipeline
            ↓
    Hallucination Verification
            ↓
    Save Assistant Message
            ↓
    Return Response
    """

    def chat(
        self,
        query,
        session_id=None,
    ):

        logger.info(
            "Starting chat pipeline."
        )

        # ---------------------------------
        # Load or Create Session
        # ---------------------------------

        if session_id:

            try:

                session = ChatSession.objects.get(
                    id=session_id
                )

                logger.info(
                    "Loaded existing session %s",
                    session.id
                )

            except ChatSession.DoesNotExist:

                logger.warning(
                    "Session not found. Creating a new one."
                )

                session = create_session()

        else:

            logger.info(
                "Creating a new chat session."
            )

            session = create_session()

        # ---------------------------------
        # Save User Message
        # ---------------------------------

        add_message(
            session=session,
            role="user",
            content=query,
        )

        # ---------------------------------
        # Load Conversation History
        # ---------------------------------

        history = get_history(session)

        # ---------------------------------
        # Rewrite Query
        # ---------------------------------

        rewritten_query = rewrite_query(
            query=query,
            memory=history,
        )

        logger.info(
            "Using rewritten query: %s",
            rewritten_query,
        )

        # ---------------------------------
        # Ask EKDE
        # ---------------------------------

        with Timer() as timer:

            response = ask_ekde(
                query=rewritten_query,
                history=history,
            )


        # ---------------------------------
        # Verify Answer
        # ---------------------------------

        verified = verify_answer(
            answer=response["answer"],
            context=response["context"],
            confidence=response["confidence"],
        )

        response["answer"] = verified["answer"]
        response["confidence"] = verified["confidence"]

        log_search(
            query=query,
            intent=detect_intent(query),
            source=detect_source(query),
            confidence=response["confidence"],
            retrieved_chunks=len(
                response["citations"]
            ),
            response_time=timer.elapsed,
        )

        # ---------------------------------
        # Save Assistant Response
        # ---------------------------------

        add_message(
            session=session,
            role="assistant",
            content=response["answer"],
        )

        # ---------------------------------
        # Attach Session ID
        # ---------------------------------

        response["session_id"] = session.id

        logger.info(
            "Chat pipeline completed."
        )

        return response


chatbot = ChatPipeline()