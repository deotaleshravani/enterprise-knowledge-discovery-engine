import logging

logger = logging.getLogger(__name__)


def format_pdf(document):
    """
    Formats PDF documents into
    structured enterprise-friendly text.
    """

    metadata = document.metadata

    document_id = metadata.get(
        "id",
        document.id
    )

    source_folder = metadata.get(
        "source_folder",
        "Unknown"
    )

    content = metadata.get(
        "text",
        document.text
    )

    parts = []

    parts.append(
        "==================== PDF DOCUMENTATION ===================="
    )

    parts.append(
        f"Document ID: {document_id}"
    )

    parts.append(
        "Document Type: PDF"
    )

    parts.append(
        f"Source Category: {source_folder}"
    )

    parts.append(
        f"Content:\n{content}"
    )

    parts.append(
        "============================================================"
    )

    formatted = "\n\n".join(parts)

    logger.info(
        "Formatted PDF document %s",
        document.id
    )

    return formatted