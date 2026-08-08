import logging

logger = logging.getLogger(__name__)


INTENT_PATTERNS = {
    "PERSON": [
        "who",
        "created by",
        "author",
        "owner",
        "assigned",
        "assignee",
        "engineer",
        "developer",
        "user",
        "person",
        "employee",
        "manager",
        "lead",
        "attendee",
    ],

    "TEAM": [
        "team",
        "group",
        "department",
        "project",
        "channel",
    ],

    "DATE": [
        "when",
        "date",
        "created",
        "updated",
        "resolved",
        "timestamp",
        "time",
    ],

    "STATUS": [
        "status",
        "open",
        "closed",
        "resolved",
        "progress",
        "in progress",
        "pending",
        "completed",
    ],

    "PRIORITY": [
        "priority",
        "severity",
        "critical",
        "high",
        "medium",
        "low",
    ],

    "TECHNOLOGY": [
        "technology",
        "framework",
        "database",
        "language",
        "postgresql",
        "redis",
        "kubernetes",
        "docker",
        "rabbitmq",
        "angular",
    ],

    "ROOT_CAUSE": [
        "root cause",
        "why",
        "reason",
        "cause",   
        "problem",
        "issue",
        "failure",
        "bug",
        "error",        
    ],

    "SUMMARY": [
        "summary",
        "summarize",
        "overview",
        "decision",
    ],

    "ROLE":[
        "role",
        "engineer",
        "developer",
        "qa",
        "architect",
        "manager",

    ],

    "MEETING":[
        "meeting",
        "meeting notes",
        "attendees",
        "discussion",
    ]



}


def detect_intent(query):
    """
    Detects the user's information intent.
    """

    query = query.lower()

    for intent, keywords in INTENT_PATTERNS.items():

        for keyword in keywords:

            if keyword in query:

                logger.info(
                    "Detected intent: %s",
                    intent
                )

                return intent

    logger.info(
        "Detected intent: GENERAL"
    )

    return "GENERAL"