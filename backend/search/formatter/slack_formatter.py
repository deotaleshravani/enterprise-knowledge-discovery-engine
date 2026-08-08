def format_slack(document):
    """
    Formats Slack messages into
    structured text.
    """

    metadata = document.metadata

    parts = []

    parts.append(
        f"Slack Message ID: {metadata.get('message_id', document.id)}"
    )

    parts.append(
        f"Channel: {metadata.get('channel', 'Unknown')}"
    )

    parts.append(
        f"Author: {metadata.get('author', 'Unknown')}"
    )

    parts.append(
        f"Team: {metadata.get('team', 'Unknown')}"
    )

    parts.append(
        f"Date: {metadata.get('date', 'Unknown')}"
    )

    parts.append(
        f"Message: {document.text}"
    )

    return "\n".join(parts)