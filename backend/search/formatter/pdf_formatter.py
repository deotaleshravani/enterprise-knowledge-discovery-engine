def format_pdf(document):
    """
    Formats PDF documents into
    structured text.
    """

    metadata = document.metadata

    parts = []

    parts.append(
        f"Document ID: {document.id}"
    )

    parts.append(
        f"Title: {metadata.get('title', 'Unknown')}"
    )

    parts.append(
        f"Category: {metadata.get('category', 'Unknown')}"
    )

    parts.append(
        f"Author: {metadata.get('author', 'Unknown')}"
    )

    parts.append(
        f"Content:\n{document.text}"
    )

    return "\n".join(parts)