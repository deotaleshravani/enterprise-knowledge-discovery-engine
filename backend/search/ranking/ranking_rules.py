from datetime import datetime


# --------------------------------------------------
# Enterprise Source Priority
# --------------------------------------------------

SOURCE_PRIORITY = {

    "jira": 0.20,

    "meeting": 0.15,

    "pdf": 0.10,

    "slack": 0.05,
}


def source_bonus(source):
    """
    Returns the priority bonus
    for a document source.
    """

    if not source:

        return 0

    return SOURCE_PRIORITY.get(
        source.lower(),
        0
    )


# --------------------------------------------------
# Freshness Bonus
# --------------------------------------------------

def freshness_bonus(date_string):
    """
    Gives newer documents
    a slightly higher score.

    Maximum bonus = 0.10
    """

    if not date_string:

        return 0

    try:

        date = datetime.fromisoformat(
            str(date_string)
        )

    except Exception:

        return 0

    today = datetime.now()

    age = (
        today - date
    ).days

    if age <= 30:

        return 0.10

    if age <= 180:

        return 0.07

    if age <= 365:

        return 0.05

    return 0