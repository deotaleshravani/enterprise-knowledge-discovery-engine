from unittest.mock import patch

from django.test import SimpleTestCase

from chatbot.llm.ollama_client import ask_llm


class OllamaClientTests(SimpleTestCase):
    """
    Unit tests for the Ollama client.
    """

    @patch("chatbot.llm.ollama_client.ollama.chat")
    def test_successful_response(
        self,
        mock_chat
    ):
        """
        Ollama should return the generated text.
        """

        mock_chat.return_value = {
            "message": {
                "content": "Hello from Llama"
            }
        }

        response = ask_llm("Hello")

        self.assertEqual(
            response,
            "Hello from Llama"
        )

    @patch("chatbot.llm.ollama_client.ollama.chat")
    def test_connection_failure(
        self,
        mock_chat
    ):
        """
        Connection failures should raise RuntimeError.
        """

        mock_chat.side_effect = Exception(
            "Cannot connect"
        )

        with self.assertRaises(RuntimeError):

            ask_llm("Hello")