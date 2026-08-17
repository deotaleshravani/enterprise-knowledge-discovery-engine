from unittest.mock import patch

from django.test import SimpleTestCase

from chatbot.rag_pipeline import ask_ekde


class RagPipelineTests(SimpleTestCase):
    """
    Unit tests for the EKDE RAG pipeline.
    """

    @patch("chatbot.rag_pipeline.ask_llm")
    @patch("chatbot.rag_pipeline.create_prompt")
    @patch("chatbot.rag_pipeline.build_context")
    def test_successful_pipeline(
        self,
        mock_build_context,
        mock_create_prompt,
        mock_ask_llm
    ):
        """
        Pipeline should combine retrieval,
        prompt creation and LLM generation.
        """

        mock_build_context.return_value = {
            "context": "Database context",
            "citations": [
                {
                    "document_id": "DOC-001",
                    "source": "pdf"
                }
            ],
            "confidence": 91
        }

        mock_create_prompt.return_value = "Prompt"

        mock_ask_llm.return_value = (
            "This is the answer."
        )

        response = ask_ekde(
            query="What is EKDE?"
        )

        self.assertEqual(
            response["answer"],
            "This is the answer."
        )

        self.assertEqual(
            response["confidence"],
            91
        )

        self.assertEqual(
            len(response["citations"]),
            1
        )

        self.assertEqual(
            response["context"],
            "Database context"
        )

    @patch("chatbot.rag_pipeline.ask_llm")
    @patch("chatbot.rag_pipeline.create_prompt")
    @patch("chatbot.rag_pipeline.build_context")
    def test_empty_context(
        self,
        mock_build_context,
        mock_create_prompt,
        mock_ask_llm
    ):
        """
        Empty retrieval should still
        return an LLM response.
        """

        mock_build_context.return_value = {
            "context": "",
            "citations": [],
            "confidence": 0
        }

        mock_create_prompt.return_value = "Prompt"

        mock_ask_llm.return_value = (
            "I could not find relevant information."
        )

        response = ask_ekde(
            query="Unknown"
        )

        self.assertEqual(
            response["confidence"],
            0
        )

        self.assertEqual(
            len(response["citations"]),
            0
        )

        self.assertEqual(
            response["answer"],
            "I could not find relevant information."
        )