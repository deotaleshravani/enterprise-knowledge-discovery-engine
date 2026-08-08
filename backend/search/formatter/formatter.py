from search.formatter.jira_formatter import format_jira
from search.formatter.slack_formatter import format_slack
from search.formatter.meeting_formatter import format_meeting
from search.formatter.pdf_formatter import format_pdf


def format_document(document):
    """
    Routes a document to the correct formatter
    based on its source.
    """

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