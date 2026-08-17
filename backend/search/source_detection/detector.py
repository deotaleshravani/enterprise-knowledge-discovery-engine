import logging

logger = logging.getLogger(__name__)


SOURCE_KEYWORDS = {
    "jira": [
        "jira",
        "ticket",
        "tickets",
        "issue",
        "issues",
        "bug",
        "bugs",
    ],

    "slack": [
        "slack",
        "chat",
        "conversation",
        "conversations",
        "message",
        "messages",
    ],

    "meeting": [
        "meeting",
        "meetings",
        "minutes",
        "discussion",
        "discussions",
        "call",
        "calls",
    ],

    "pdf": [
        "pdf",
        "document",
        "documents",
        "manual",
        "manuals",
        "guide",
        "guides",
        "report",
        "reports",
    ],
}


def detect_source(query):
    """
    Detects whether the user wants to search
    a specific enterprise source.

    Returns:

        "jira"

        "slack"

        "meeting"

        "pdf"

        None
    """

    query = query.lower()

    for source, keywords in SOURCE_KEYWORDS.items():

        for keyword in keywords:

            if keyword in query:

                logger.info(
                    "Detected source: %s",
                    source,
                )

                return source

    logger.info(
        "No specific source detected."
    )

    return None