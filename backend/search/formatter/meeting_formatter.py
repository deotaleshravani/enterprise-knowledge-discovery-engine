import logging

logger = logging.getLogger(__name__)


def format_meeting(document):
    """
    Converts meeting notes into a structured,
    enterprise-friendly representation for the LLM.
    """

    metadata = document.metadata

    meeting_id = metadata.get(
        "meeting_id",
        document.id
    )

    meeting_type = metadata.get(
        "meeting_type",
        "Unknown"
    )

    project = metadata.get(
        "project",
        "Unknown"
    )

    team = metadata.get(
        "team",
        "Unknown"
    )

    technology = metadata.get(
        "technology",
        "Unknown"
    )

    attendees = metadata.get(
        "attendees",
        []
    )

    topic = metadata.get(
        "topic",
        "Unknown"
    )

    decision = metadata.get(
        "decision",
        "Not specified"
    )

    summary = metadata.get(
        "summary",
        document.text
    )

    related_ticket = metadata.get(
        "related_ticket",
        "None"
    )

    date = metadata.get(
        "date",
        "Unknown"
    )

    attendees_text = ", ".join(
        attendees
    ) if attendees else "None"

    formatted = f"""
==================== MEETING NOTES ====================

MEETING ID
{meeting_id}

MEETING TYPE
{meeting_type}

PROJECT
{project}

TEAM
{team}

TECHNOLOGY
{technology}

DATE
{date}

ATTENDEES
{attendees_text}

TOPIC
{topic}

RELATED JIRA TICKET
{related_ticket}

DECISION
{decision}

SUMMARY
{summary}

========================================================
"""

    logger.info(
        "Formatted Meeting document %s",
        document.id
    )

    return formatted.strip()