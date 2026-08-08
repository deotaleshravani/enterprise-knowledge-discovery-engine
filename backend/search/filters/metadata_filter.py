import logging

logger = logging.getLogger(__name__)


def apply_filters(results, query):
    """
    Filters retrieved results using
    metadata keywords found in the query.
    """

    query = query.lower()

    filtered = []

    priorities = [
        "critical",
        "high",
        "medium",
        "low",
    ]

    statuses = [
        "open",
        "closed",
        "resolved",
        "in progress",
    ]

    teams = [
        "backend alpha",
        "frontend beta",
        "platform",
        "devops",
    ]

    technologies = [
        "postgresql",
        "kubernetes",
        "redis",
        "docker",
    ]

    for result in results:

        text = result["text"].lower()

        keep = True

        for priority in priorities:

            if priority in query and priority not in text:
                keep = False

        for status in statuses:

            if status in query and status not in text:
                keep = False

        for team in teams:

            if team in query and team not in text:
                keep = False

        for tech in technologies:

            if tech in query and tech not in text:
                keep = False

        if keep:
            filtered.append(result)

    logger.info(
        "Metadata filter reduced %d results to %d.",
        len(results),
        len(filtered),
    )

    return filtered if filtered else results