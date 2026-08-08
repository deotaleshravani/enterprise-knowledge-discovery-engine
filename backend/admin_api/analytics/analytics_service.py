from collections import Counter

from django.db.models import Avg

from search.models import SearchAnalytics


def get_search_analytics():
    """
    Returns enterprise search analytics.
    """

    searches = SearchAnalytics.objects.all()

    total = searches.count()

    average_confidence = (

        searches.aggregate(
            Avg("confidence")
        )["confidence__avg"]

        or 0
    )

    average_response = (

        searches.aggregate(
            Avg("response_time")
        )["response_time__avg"]

        or 0
    )

    query_counter = Counter(

        searches.values_list(
            "query",
            flat=True,
        )

    )

    intent_counter = Counter(

        searches.values_list(
            "intent",
            flat=True,
        )

    )

    source_counter = Counter(

        searches.values_list(
            "source",
            flat=True,
        )

    )

    return {

        "total_searches": total,

        "average_confidence": round(
            average_confidence,
            2,
        ),

        "average_response_time": round(
            average_response,
            3,
        ),

        "top_queries":

            query_counter.most_common(10),

        "intent_distribution":

            dict(intent_counter),

        "source_distribution":

            dict(source_counter),

    }