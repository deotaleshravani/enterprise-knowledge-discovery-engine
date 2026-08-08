import logging

logger = logging.getLogger(__name__)


INTENT_FIELDS = {

    "PERSON": [
        "created by",
        "author",
        "owner",
        "assigned",
        "assignee",
        "engineer",
        "developer",
        "role",
    ],

    "TEAM": [
        "team",
        "department",
        "group",
    ],

    "DATE": [
        "created",
        "updated",
        "resolved",
        "date",
        "timestamp",
    ],

    "STATUS": [
        "status",
        "resolved",
        "closed",
        "open",
    ],

    "PRIORITY": [
        "priority",
        "critical",
        "severity",
        "high",
        "medium",
        "low",
    ],

    "TECHNOLOGY": [
        "technology",
        "postgresql",
        "docker",
        "redis",
        "kubernetes",
        "framework",
    ],

    "ROOT_CAUSE": [
        "root cause",
        "reason",
        "cause",
    ],
}


def boost_results(results, intent):
    """
    Boosts retrieval scores using metadata
    relevant to the detected intent.
    """

    if intent == "GENERAL":

        return results

    keywords = INTENT_FIELDS.get(
        intent,
        []
    )

    for result in results:

        score = result.get(
            "final_score",
            0
        )

        text = result["text"].lower()

        boost = 0

        for keyword in keywords:

            if keyword in text:

                boost += 10

        result["final_score"] = score + boost

    results.sort(
        key=lambda x: x["final_score"],
        reverse=True
    )

    logger.info(
        "Metadata boosting applied for %s.",
        intent
    )

    return results