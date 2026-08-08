def format_meeting(document):
    """
    Formats meeting notes into
    structured text.
    """

    metadata = document.metadata

    parts = []

    parts.append(
        f"Meeting ID: {metadata.get('meeting_id', document.id)}"
    )

    parts.append(
        f"Title: {metadata.get('title', 'Unknown')}"
    )

    parts.append(
        f"Team: {metadata.get('team', 'Unknown')}"
    )

    parts.append(
        f"Organizer: {metadata.get('organizer', 'Unknown')}"
    )

    parts.append(
        f"Date: {metadata.get('date', 'Unknown')}"
    )

    parts.append(
        f"Discussion:\n{document.text}"
    )

    return "\n".join(parts)