import logging

logger = logging.getLogger(__name__)


def format_jira(document):
    """
    Formats a Jira ticket into an
    LLM-friendly enterprise context.
    """

    metadata = document.metadata

    ticket_id = metadata.get(
        "ticket_id",
        document.id,
    )

    title = metadata.get("title", "")

    description = metadata.get(
        "description",
        ""
    )

    resolution = metadata.get(
        "resolution",
        ""
    )

    project = metadata.get(
        "project",
        ""
    )

    team = metadata.get(
        "team",
        ""
    )

    category = metadata.get(
        "category",
        ""
    )

    technology = metadata.get(
        "technology",
        ""
    )

    priority = metadata.get(
        "priority",
        ""
    )

    status = metadata.get(
        "status",
        ""
    )

    created_by = metadata.get(
        "created_by",
        ""
    )

    creator_role = metadata.get(
        "creator_role",
        ""
    )

    created_date = metadata.get(
        "created_date",
        ""
    )

    formatted = f"""
### Jira Ticket

Ticket ID: {ticket_id}

Title: {title}

Project: {project}

Team: {team}

Category: {category}

Technology: {technology}

Priority: {priority}

Status: {status}

Created By: {created_by}

Role: {creator_role}

Created Date: {created_date}

Description:
{description}

Resolution:
{resolution}

Instructions for the AI:
When using information from this ticket,
refer to it naturally as:

"According to Jira Ticket {ticket_id}..."

or

"The Jira ticket titled '{title}' indicates..."

Avoid referring to it as only a document or source.
"""

    logger.info(
        "Formatted Jira document %s",
        document.id,
    )

    return formatted.strip()