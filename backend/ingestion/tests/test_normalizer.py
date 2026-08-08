from django.test import SimpleTestCase

from ingestion.services.normalizer import normalize


class NormalizerTests(SimpleTestCase):
    """
    Unit tests for the normalize() function.
    """

    # -------------------------------------------------
    # Jira
    # -------------------------------------------------

    def test_normalize_jira_document(self):

        raw = {
            "ticket_id": "JIRA-0001",
            "title": "JWT Authentication",
            "description": "Users cannot login.",
            "resolution": "Updated refresh token logic.",
            "created_by": "Alice",
            "created_date": "2026-01-15"
        }

        doc = normalize(raw, "jira")

        self.assertEqual(doc["id"], "JIRA-0001")
        self.assertEqual(doc["source"], "jira")
        self.assertEqual(doc["author"], "Alice")
        self.assertIn("JWT Authentication", doc["text"])
        self.assertIsNotNone(doc["date"])
        self.assertEqual(doc["metadata"], raw)

    # -------------------------------------------------
    # Slack
    # -------------------------------------------------

    def test_normalize_slack_document(self):

        raw = {
            "message_id": "SLK-0001",
            "user": "John",
            "message": "Refresh token issue resolved.",
            "timestamp": "2026-02-10"
        }

        doc = normalize(raw, "slack")

        self.assertEqual(doc["id"], "SLK-0001")
        self.assertEqual(doc["source"], "slack")
        self.assertEqual(doc["author"], "John")
        self.assertEqual(
            doc["text"],
            "Refresh token issue resolved."
        )

    # -------------------------------------------------
    # Meeting
    # -------------------------------------------------

    def test_normalize_meeting_document(self):

        raw = {
            "meeting_id": "MTG-001",
            "topic": "Authentication",
            "summary": "Refresh tokens discussed.",
            "decision": "Enable token rotation.",
            "attendees": ["Alice", "Bob"],
            "date": "2026-03-01"
        }

        doc = normalize(raw, "meeting")

        self.assertEqual(doc["id"], "MTG-001")
        self.assertEqual(doc["source"], "meeting")
        self.assertEqual(doc["author"], "Alice, Bob")
        self.assertIn("Authentication", doc["text"])
        self.assertIn("Enable token rotation.", doc["text"])

    # -------------------------------------------------
    # PDF
    # -------------------------------------------------

    def test_normalize_pdf_document(self):

        raw = {
            "id": "PDF-001",
            "text": "OAuth architecture documentation.",
            "author": "System",
            "date": "2026-04-01"
        }

        doc = normalize(raw, "pdf")

        self.assertEqual(doc["id"], "PDF-001")
        self.assertEqual(doc["source"], "pdf")
        self.assertEqual(doc["author"], "System")
        self.assertEqual(
            doc["text"],
            "OAuth architecture documentation."
        )

    # -------------------------------------------------
    # Unknown Source
    # -------------------------------------------------

    def test_unknown_source(self):

        raw = {
            "id": "ABC-001",
            "text": "Sample document",
            "author": "Unknown"
        }

        doc = normalize(raw, "random_source")

        self.assertEqual(doc["id"], "ABC-001")
        self.assertEqual(doc["source"], "random_source")
        self.assertEqual(doc["author"], "Unknown")

    # -------------------------------------------------
    # Missing Optional Fields
    # -------------------------------------------------

    def test_missing_optional_fields(self):

        raw = {
            "ticket_id": "JIRA-002"
        }

        doc = normalize(raw, "jira")

        self.assertEqual(doc["id"], "JIRA-002")
        self.assertEqual(doc["author"], "Unknown")
        self.assertEqual(doc["text"], "")

    # -------------------------------------------------
    # Empty Text Cleaning
    # -------------------------------------------------

    def test_empty_text(self):

        raw = {
            "id": "PDF-002",
            "text": ""
        }

        doc = normalize(raw, "pdf")

        self.assertEqual(doc["text"], "")