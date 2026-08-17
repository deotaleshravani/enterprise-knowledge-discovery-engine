def explain_search_results(query, results):
    """
    Explain why a query matched the retrieved enterprise documents.

    This helper reads the strongest metadata fields from search results and
    returns a structured explanation suitable for API responses and UI display.
    """
    explanation = {
        "query": query,
        "summary": "Matched because relevant enterprise metadata aligns with the query.",
        "matched": [],
    }

    if not results:
        explanation["summary"] = "No relevant enterprise content matched the query."
        return explanation

    for result in results[:5]:
        metadata = result.get("metadata", {}) or {}
        if not metadata and result.get("source"):
            metadata = {"source": result.get("source")}

        score = result.get("score") or result.get("final_score") or 0
        technology = metadata.get("technology") or metadata.get("tech")
        priority = metadata.get("priority")
        creator = metadata.get("created_by") or metadata.get("user") or metadata.get("author")
        title = metadata.get("title") or metadata.get("topic") or metadata.get("message")

        candidate_fields = [
            ("Technology", technology),
            ("Priority", priority),
            ("Creator", creator),
            ("Title", title),
        ]

        for field_name, value in candidate_fields:
            if value and str(value).lower() in str(query).lower():
                explanation["matched"].append({
                    "field": field_name,
                    "value": value,
                    "score": round(float(score), 3),
                    "source": result.get("source", "unknown"),
                    "document_id": result.get("document_id"),
                })

        if not explanation["matched"] and score:
            explanation["matched"].append({
                "field": "Similarity",
                "value": round(float(score), 3),
                "score": round(float(score), 3),
                "source": result.get("source", "unknown"),
                "document_id": result.get("document_id"),
            })

    if not explanation["matched"]:
        explanation["summary"] = "The query matched a weak retrieval signal but not a strong enterprise metadata match."
    else:
        top_match = explanation["matched"][0]
        explanation["summary"] = (
            f"Matched because {top_match['field']} = {top_match['value']} "
            f"with similarity {top_match['score']}"
        )

    return explanation
