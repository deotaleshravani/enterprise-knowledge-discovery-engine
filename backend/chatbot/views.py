import logging
from chatbot.models import ChatSession
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from chatbot.serializers import (
    ChatRequestSerializer,
    ChatResponseSerializer,
    ChatSessionSerializer,
    ChatMessageSerializer,
)

from chatbot.services.session_service import (
    get_all_sessions,
    get_session,
    rename_session,
    delete_session,
)

from chatbot.chat_pipeline import chatbot

logger = logging.getLogger(__name__)


class ChatAPIView(APIView):
    """
    POST /api/chat/

    Accepts
    -------
    question
    session_id (optional)

    Returns
    -------
    answer
    citations
    confidence
    session_id (later)
    """

    def post(self, request):

        logger.info(
            "Received new chat request."
        )

        # ---------------------------------
        # Validate request
        # ---------------------------------

        serializer = ChatRequestSerializer(
            data=request.data
        )

        if not serializer.is_valid():

            logger.warning(
                "Invalid chat request received: %s",
                serializer.errors
            )

            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )

        data = serializer.validated_data

        logger.info(
            "Question: %s",
            data["question"]
        )

        # ---------------------------------
        # Run Chat Pipeline
        # ---------------------------------

        try:

            result = chatbot.chat(
                data["question"],
                session_id=data.get("session_id"),
            )

        except RuntimeError as error:

            logger.exception(
                "LLM service unavailable."
            )

            return Response(
                {
                    "error": str(error)
                },
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        except Exception:

            logger.exception(
                "Unexpected server error."
            )

            return Response(
                {
                    "error":
                    "An unexpected server error occurred."
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # ---------------------------------
        # Serialize response
        # ---------------------------------

        response = ChatResponseSerializer(
            result
        )

        logger.info(
            "Chat request completed successfully."
        )

        return Response(
            response.data,
            status=status.HTTP_200_OK
        )

class SessionListAPIView(APIView):

    def get(self, request):

        sessions = get_all_sessions()

        serializer = ChatSessionSerializer(
            sessions,
            many=True,
        )

        return Response(serializer.data)


class SessionDetailAPIView(APIView):

    def get(
        self,
        request,
        session_id,
    ):

        session = get_session(session_id)

        messages = session.messages.order_by(
            "created_at"
        )

        return Response({

            "session": ChatSessionSerializer(
                session
            ).data,

            "messages": ChatMessageSerializer(
                messages,
                many=True,
            ).data,
        })


class RenameSessionAPIView(APIView):

    def put(
        self,
        request,
        session_id,
    ):

        session = get_session(session_id)

        rename_session(
            session,
            request.data["title"],
        )

        return Response({
            "message": "Session renamed."
        })


class DeleteSessionAPIView(APIView):

    def delete(
        self,
        request,
        session_id,
    ):

        session = get_session(session_id)

        delete_session(session)

        return Response({
            "message": "Session deleted."
        })
        
class ChatHistoryAPIView(APIView):
    """
    GET /api/chat/history/<session_id>/

    Returns all messages belonging to
    a chat session.
    """

    def get(
        self,
        request,
        session_id,
    ):

        try:

            session = ChatSession.objects.get(
                id=session_id
            )

        except ChatSession.DoesNotExist:

            return Response(
                {
                    "error": "Session not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        history = []

        for message in session.messages.order_by(
            "created_at"
        ):

            history.append({

                "role": message.role,

                "content": message.content,

                "created_at": message.created_at,

            })

        return Response(
            history,
            status=status.HTTP_200_OK
        )