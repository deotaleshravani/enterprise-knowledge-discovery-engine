import logging
import time

from search.models import SearchAnalytics

logger = logging.getLogger(__name__)


def log_search(
    query,
    intent,
    source,
    confidence,
    retrieved_chunks,
    response_time,
):
    """
    Stores analytics for every enterprise search.
    """

    SearchAnalytics.objects.create(

        query=query,

        intent=intent,

        source=source or "",

        confidence=confidence,

        retrieved_chunks=retrieved_chunks,

        response_time=response_time,

    )

    logger.info(
        "Search analytics stored."
    )


class Timer:
    """
    Measures search response time.
    """

    def __enter__(self):

        self.start = time.perf_counter()

        return self

    def __exit__(self, *args):

        self.end = time.perf_counter()

        self.elapsed = round(
            self.end - self.start,
            3,
        )