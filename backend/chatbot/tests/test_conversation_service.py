from unittest.mock import MagicMock
from unittest.mock import patch

from django.test import SimpleTestCase

from chatbot.services.conversation_service import chat


class ConversationServiceTests(SimpleTestCase):
    """
    Unit tests for the conversation service.
    """

    @patch("chatbot.services.conversation_service.add_message")
    @patch("chatbot.services.conversation_service.ask_ekde")
    @patch("chatbot.services.conversation_service.get_history")
    @patch("chatbot.services.conversation_service.create_session")
    def test_new_chat_session(
        self,
        mock_create_session,
        mock_get_history,
        mock_ask_ekde,
        mock_add_message,
    ):
        """
        A new session should be created when
        no session_id is provided.
        """

        session = MagicMock()
        session.id = "session-123"

        mock_create_session.return_value = session

        mock_get_history.return_value = ""

        mock_ask_ekde.return_value = {
            "answer": "EKDE Answer",
            "citations": [],
            "confidence": 90,
        }

        response = chat(
            query="What is EKDE?"
        )

        self.assertEqual(
            response["answer"],
            "EKDE Answer"
        )

        self.assertEqual(
            response["confidence"],
            90
        )

        self.assertEqual(
            response["session_id"],
            "session-123"
        )

        self.assertEqual(
            mock_add_message.call_count,
            2
        )

    @patch("chatbot.services.conversation_service.add_message")
    @patch("chatbot.services.conversation_service.ask_ekde")
    @patch("chatbot.services.conversation_service.get_history")
    @patch("chatbot.services.conversation_service.ChatSession")
    def test_existing_chat_session(
        self,
        mock_chat_session,
        mock_get_history,
        mock_ask_ekde,
        mock_add_message,
    ):
        """
        Existing sessions should be reused.
        """

        session = MagicMock()
        session.id = "existing-session"

        mock_chat_session.objects.get.return_value = (
            session
        )

        mock_get_history.return_value = (
            "Previous conversation"
        )

        mock_ask_ekde.return_value = {
            "answer": "Existing Answer",
            "citations": [],
            "confidence": 80,
        }

        response = chat(
            query="Next question",
            session_id="existing-session",
        )

        self.assertEqual(
            response["session_id"],
            "existing-session"
        )

        self.assertEqual(
            response["answer"],
            "Existing Answer"
        )

        self.assertEqual(
            mock_add_message.call_count,
            2
        )