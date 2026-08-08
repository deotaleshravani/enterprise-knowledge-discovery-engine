from unittest.mock import patch

from django.urls import reverse

from rest_framework import status
from rest_framework.test import APITestCase


class ChatAPIViewTests(APITestCase):
    """
    Tests for the Chat API endpoint.
    """

    @patch("chatbot.views.chat")
    def test_chat_success(
        self,
        mock_chat
    ):
        """
        Valid requests should return a
        successful chatbot response.
        """

        mock_chat.return_value = {
            "answer": "Hello!",
            "confidence": 95,
            "session_id": "123e4567-e89b-12d3-a456-426614174000",
            "citations": []
        }

        response = self.client.post(
            reverse("chat"),
            {
                "question": "Hello"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["answer"],
            "Hello!"
        )

    @patch("chatbot.views.chat")
    def test_chat_runtime_error(
        self,
        mock_chat
    ):
        """
        RuntimeError should return HTTP 503.
        """

        mock_chat.side_effect = RuntimeError(
            "Ollama unavailable"
        )

        response = self.client.post(
            reverse("chat"),
            {
                "question": "Hello"
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_503_SERVICE_UNAVAILABLE
        )

    def test_invalid_request(self):
        """
        Missing question should return 400.
        """

        response = self.client.post(
            reverse("chat"),
            {},
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST
        )

    @patch("chatbot.views.chat")
    def test_existing_session(
        self,
        mock_chat
    ):
        """
        Existing session IDs should be accepted.
        """

        session_id = (
            "123e4567-e89b-12d3-a456-426614174000"
        )

        mock_chat.return_value = {
            "answer": "Welcome back!",
            "confidence": 92,
            "session_id": session_id,
            "citations": []
        }

        response = self.client.post(
            reverse("chat"),
            {
                "question": "Hello again",
                "session_id": session_id
            },
            format="json"
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK
        )

        self.assertEqual(
            response.data["session_id"],
            session_id
        )