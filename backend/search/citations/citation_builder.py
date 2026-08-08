from documents.models import Document


def build_citation(document, score=0):
    """
    Builds a rich source-aware citation
    based on the document source.
    """

    metadata = document.metadata
    source = document.source.lower()

    if source == "jira":

        return {
            "source": "Jira",
            "document_id": document.id,
            "title": metadata.get("title"),
            "project": metadata.get("project"),
            "team": metadata.get("team"),
            "technology": metadata.get("technology"),
            "priority": metadata.get("priority"),
            "status": metadata.get("status"),
            "created_by": metadata.get("created_by"),
            "score": round(score, 3),
        }

    if source == "slack":

        return {
            "source": "Slack",
            "document_id": document.id,
            "channel": metadata.get("channel"),
            "author": metadata.get("author"),
            "timestamp": metadata.get("timestamp"),
            "technology": metadata.get("technology"),
            "score": round(score, 3),
        }

    if source == "meeting":

        return {
            "source": "Meeting",
            "document_id": document.id,
            "meeting_title": metadata.get("meeting_title"),
            "meeting_date": metadata.get("meeting_date"),
            "participants": metadata.get("participants"),
            "technology": metadata.get("technology"),
            "score": round(score, 3),
        }

    if source == "pdf":

        return {
            "source": "PDF",
            "document_id": document.id,
            "title": metadata.get("title"),
            "category": metadata.get("category"),
            "technology": metadata.get("technology"),
            "score": round(score, 3),
        }

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
                score=result.get("final_score", 0),
            )
        )

    return citations