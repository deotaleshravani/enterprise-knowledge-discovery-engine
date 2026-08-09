import logging

logger = logging.getLogger(__name__)


def format_slack(document):
    """
    Converts a Slack message into a structured,
    enterprise-friendly representation for the LLM.
    """

    metadata = document.metadata

    message_id = metadata.get(
        "message_id",
        document.id
    )

    channel = metadata.get(
        "channel",
        "Unknown"
    )

    user = metadata.get(
        "user",
        "Unknown"
    )

    role = metadata.get(
        "role",
        "Unknown"
    )

    team = metadata.get(
        "team",
        "Unknown"
    )

    project = metadata.get(
        "project",
        "Unknown"
    )

    technology = metadata.get(
        "technology",
        "Unknown"
    )

    related_ticket = metadata.get(
        "related_ticket",
        "None"
    )

    timestamp = metadata.get(
        "timestamp",
        "Unknown"
    )

    message = metadata.get(
        "message",
        document.text
    )

    formatted = f"""
==================== SLACK DISCUSSION ====================

MESSAGE ID
{message_id}

CHANNEL
{channel}

AUTHOR
{user}

ROLE
{role}

TEAM
{team}

PROJECT
{project}

TECHNOLOGY
{technology}

RELATED JIRA TICKET
{related_ticket}

TIMESTAMP
{timestamp}

MESSAGE
{message}

===========================================================
"""

    logger.info(
        "Formatted Slack document %s",
        document.id
    )

    return formatted.strip()