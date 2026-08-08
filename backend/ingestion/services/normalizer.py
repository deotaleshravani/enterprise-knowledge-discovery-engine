from datetime import datetime, time

from django.utils.dateparse import parse_date, parse_datetime

from ingestion.utils.text_cleaner import clean_text


def _parse_date(value):
    if not value:
        return None
    if isinstance(value, datetime):
        return value

    text = str(value)
    parsed = parse_datetime(text)
    if parsed:
        return parsed

    date_only = parse_date(text)
    if date_only:
        return datetime.combine(date_only, time.min)

    return None


def _extract_fields(raw_doc, source):
    if source == "jira":
        return {
            "id": raw_doc.get("ticket_id"),
            "text": " ".join(
                part
                for part in [
                    raw_doc.get("title", ""),
                    raw_doc.get("description", ""),
                    raw_doc.get("resolution", ""),
                ]
                if part
            ),
            "author": raw_doc.get("created_by", "Unknown"),
            "date": _parse_date(raw_doc.get("created_date")),
        }

    if source == "slack":
        return {
            "id": raw_doc.get("message_id"),
            "text": raw_doc.get("message", ""),
            "author": raw_doc.get("user", "Unknown"),
            "date": _parse_date(raw_doc.get("timestamp")),
        }

    if source == "meeting":
        attendees = raw_doc.get("attendees") or []
        return {
            "id": raw_doc.get("meeting_id"),
            "text": " ".join(
                part
                for part in [
                    raw_doc.get("topic", ""),
                    raw_doc.get("summary", ""),
                    raw_doc.get("decision", ""),
                ]
                if part
            ),
            "author": ", ".join(attendees) if attendees else "Unknown",
            "date": _parse_date(raw_doc.get("date")),
        }

    if source == "pdf":
        return {
            "id": raw_doc.get("id"),
            "text": raw_doc.get("text", ""),
            "author": raw_doc.get("author", "Unknown"),
            "date": _parse_date(raw_doc.get("date")),
        }

    return {
        "id": raw_doc.get("id"),
        "text": raw_doc.get("text", ""),
        "author": raw_doc.get("author", "Unknown"),
        "date": _parse_date(raw_doc.get("date")),
    }


def normalize(raw_doc, source):
    fields = _extract_fields(raw_doc, source)

    return {
        "id": fields["id"],
        "source": source,
        "text": clean_text(fields["text"]),
        "author": fields["author"],
        "date": fields["date"],
        "metadata": raw_doc,
    }
