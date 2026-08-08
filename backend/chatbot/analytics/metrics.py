import time


class ResponseAnalytics:
    """
    Stores runtime analytics for one query.
    """

    def __init__(self):

        self.start_time = time.perf_counter()

        self.retrieval_start = None
        self.retrieval_end = None

        self.llm_start = None
        self.llm_end = None

        self.intent = None
        self.source = None

        self.chunks_retrieved = 0
        self.chunks_used = 0
        self.documents_used = 0

    # ---------------------------------

    def start_retrieval(self):

        self.retrieval_start = time.perf_counter()

    def end_retrieval(self):

        self.retrieval_end = time.perf_counter()

    # ---------------------------------

    def start_llm(self):

        self.llm_start = time.perf_counter()

    def end_llm(self):

        self.llm_end = time.perf_counter()

    # ---------------------------------

    def build(self):

        total = (
            time.perf_counter()
            - self.start_time
        )

        retrieval = 0

        if (
            self.retrieval_start
            and
            self.retrieval_end
        ):

            retrieval = (
                self.retrieval_end
                -
                self.retrieval_start
            )

        llm = 0

        if (
            self.llm_start
            and
            self.llm_end
        ):

            llm = (
                self.llm_end
                -
                self.llm_start
            )

        return {

            "intent":
                self.intent,

            "source":
                self.source,

            "retrieval_time":
                round(
                    retrieval,
                    3
                ),

            "llm_time":
                round(
                    llm,
                    3
                ),

            "total_time":
                round(
                    total,
                    3
                ),

            "chunks_retrieved":
                self.chunks_retrieved,

            "chunks_used":
                self.chunks_used,

            "documents_used":
                self.documents_used,
        }