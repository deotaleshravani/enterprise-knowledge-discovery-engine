import logging

logger = logging.getLogger(__name__)


def diversify_results(results, k=5):
    """
    Diversify retrieved chunks so that
    multiple enterprise sources are represented.

    Example:

    Jira
    Slack
    Meeting
    PDF
    Jira
    """

    diversified = []

    used_sources = set()

    # First pass:
    # take one chunk from each source

    for result in results:

        source = result["source"]

        if source not in used_sources:

            diversified.append(result)
            used_sources.add(source)

        if len(diversified) >= k:
            break

    # Second pass:
    # fill remaining slots

    if len(diversified) < k:

        for result in results:

            if result not in diversified:

                diversified.append(result)

            if len(diversified) >= k:
                break

    logger.info(
        "Diversified %d results into %d results.",
        len(results),
        len(diversified),
    )

    return diversified