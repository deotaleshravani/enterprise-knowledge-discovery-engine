import logging

logger = logging.getLogger(__name__)


def format_jira(document):
    """
    Formats a Jira document into
    searchable enterprise text.
    """

    metadata = document.metadata

    return f"""
Source: Jira

Document ID: {document.id}

Project: {metadata.get("project", "")}
Team: {metadata.get("team", "")}
Category: {metadata.get("category", "")}
Technology: {metadata.get("technology", "")}
Priority: {metadata.get("priority", "")}
Status: {metadata.get("status", "")}

Created By: {metadata.get("created_by", "")}
Role: {metadata.get("creator_role", "")}
Experience: {metadata.get("experience_years", "")} years

Title:
{metadata.get("title", "")}

Description:
{metadata.get("description", "")}

Resolution:
{metadata.get("resolution", "")}
"""


def format_slack(document):
    """
    Formats a Slack message.
    """

    metadata = document.metadata

    return f"""
Source: Slack

Document ID: {document.id}

Channel: {metadata.get("channel", "")}
Author: {metadata.get("author", "")}
Timestamp: {metadata.get("timestamp", "")}

Message:
{document.text}
"""


def format_meeting(document):
    """
    Formats a meeting note.
    """

    metadata = document.metadata

    return f"""
Source: Meeting

Document ID: {document.id}

Meeting Title:
{metadata.get("title", "")}

Participants:
{metadata.get("participants", "")}

Date:
{metadata.get("date", "")}

Discussion:
{document.text}

Action Items:
{metadata.get("action_items", "")}
"""


def format_pdf(document):
    """
    Formats a PDF document.
    """

    metadata = document.metadata

    return f"""
Source: PDF

Document ID: {document.id}

File Name:
{metadata.get("filename", "")}

Category:
{metadata.get("category", "")}

Content:

{document.text}
"""


def build_searchable_text(document):
    """
    Returns the formatted enterprise
    document for embedding.
    """

    logger.info(
        "Formatting document %s",
        document.id
    )

    source = document.source.lower()

    if source == "jira":
        return format_jira(document)

    if source == "slack":
        return format_slack(document)

    if source == "meeting":
        return format_meeting(document)

    if source == "pdf":
        return format_pdf(document)

    return document.text