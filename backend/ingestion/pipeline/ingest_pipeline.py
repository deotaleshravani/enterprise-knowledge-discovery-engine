from documents.models import Document

from ingestion.services.jira import fetch_jira
from ingestion.services.slack import fetch_slack
from ingestion.services.meeting import fetch_meetings
from ingestion.services.pdf import fetch_pdfs

from ingestion.services.normalizer import normalize


def run_ingestion():
    documents = []

    for item in fetch_jira():
        documents.append(normalize(item, "jira"))

    for item in fetch_slack():
        documents.append(normalize(item, "slack"))

    for item in fetch_meetings():
        documents.append(normalize(item, "meeting"))

    for item in fetch_pdfs():
        documents.append(normalize(item, "pdf"))

    created_count = 0
    updated_count = 0
    skipped_count = 0

    for doc in documents:
        if not doc["id"]:
            skipped_count += 1
            print("SKIPPED (missing id):", doc["source"])
            continue

        _, created = Document.objects.update_or_create(
            id=doc["id"],
            defaults={
                "source": doc["source"],
                "text": doc["text"],
                "author": doc["author"],
                "date": doc.get("date"),
                "metadata": doc["metadata"],
            },
        )

        if created:
            created_count += 1
        else:
            updated_count += 1

    print(f"Ingestion done: created={created_count}, updated={updated_count}, skipped={skipped_count}")
    return len(documents)
