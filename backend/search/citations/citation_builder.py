from documents.models import Document


def build_citation(document, score=0):
    """
    Builds a rich, source-aware citation
    based on the actual document metadata.
    """

    metadata = document.metadata
    source = document.source.lower()

    # -----------------------------------------
    # Jira
    # -----------------------------------------

    if source == "jira":

        return {
            "source": "Jira",
            "document_id": document.id,
            "ticket_id": metadata.get("ticket_id"),
            "title": metadata.get("title"),
            "project": metadata.get("project"),
            "team": metadata.get("team"),
            "technology": metadata.get("technology"),
            "priority": metadata.get("priority"),
            "status": metadata.get("status"),
            "created_by": metadata.get("created_by"),
            "score": round(score, 3),
        }

    # -----------------------------------------
    # Slack
    # -----------------------------------------

    if source == "slack":

        return {
            "source": "Slack",
            "document_id": document.id,
            "message_id": metadata.get("message_id"),
            "channel": metadata.get("channel"),
            "author": metadata.get("user"),
            "role": metadata.get("role"),
            "team": metadata.get("team"),
            "project": metadata.get("project"),
            "timestamp": metadata.get("timestamp"),
            "technology": metadata.get("technology"),
            "related_ticket": metadata.get("related_ticket"),
            "score": round(score, 3),
        }

    # -----------------------------------------
    # Meeting
    # -----------------------------------------

    if source == "meeting":

        return {
            "source": "Meeting",
            "document_id": document.id,
            "meeting_id": metadata.get("meeting_id"),
            "meeting_type": metadata.get("meeting_type"),
            "project": metadata.get("project"),
            "team": metadata.get("team"),
            "technology": metadata.get("technology"),
            "attendees": metadata.get("attendees"),
            "topic": metadata.get("topic"),
            "decision": metadata.get("decision"),
            "related_ticket": metadata.get("related_ticket"),
            "date": metadata.get("date"),
            "score": round(score, 3),
        }

    # -----------------------------------------
    # PDF
    # -----------------------------------------

    if source == "pdf":

        return {
            "source": "PDF",
            "document_id": document.id,
            "pdf_id": metadata.get(
                "id",
                document.id
            ),
            "category": metadata.get(
                "source_folder"
            ),
            "score": round(score, 3),
        }

    # -----------------------------------------
    # Unknown source
    # -----------------------------------------

    return {
        "source": document.source,
        "document_id": document.id,
        "score": round(score, 3),
    }


def build_citations(results):
    """
    Builds citations for all retrieved documents.
    """

    citations = []

    for result in results:

        try:

            document = Document.objects.get(
                id=result["document_id"]
            )

        except Document.DoesNotExist:

            continue

        citations.append(
            build_citation(
                document,
                score=result.get(
                    "final_score",
                    0
                ),
            )
        )

    return citations