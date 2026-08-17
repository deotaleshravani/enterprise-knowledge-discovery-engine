import logging

logger = logging.getLogger(__name__)


def calculate_confidence(results):
    """
    Calculates confidence from retrieval scores.

    Workflow
    --------
    Retrieved Results
            ↓
    Read final_score
            ↓
    Average score
            ↓
    Convert to percentage
    """

    if not results:

        return 0

    # ----------------------------
    # Collect scores
    # ----------------------------

    scores = []

    for result in results:

        if "final_score" in result:

            scores.append(
                result["final_score"]
            )

        elif "score" in result:

            scores.append(
                result["score"]
            )

        elif "normalized_score" in result:

            scores.append(
                result["normalized_score"]
            )

        elif "distance" in result:

            # Fallback for old FAISS-only retrieval
            similarity = 1 / (
                1 + result["distance"]
            )

            scores.append(similarity)

    if not scores:

        return 0

    # ----------------------------
    # Average retrieval score
    # ----------------------------

    average = (
        sum(scores)
        /
        len(scores)
    )

    confidence = round(
        average * 100
    )

    confidence = max(
        0,
        min(confidence, 100)
    )

    logger.info(
        "Confidence score: %d",
        confidence
    )

    return confidence