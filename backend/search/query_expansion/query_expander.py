import logging

from search.knowledge_graph.graph_query import (
    search_graph,
    get_neighbors,
)

logger = logging.getLogger(__name__)

STOP_WORDS = {
    "who",
    "what",
    "when",
    "where",
    "why",
    "how",
    "did",
    "does",
    "is",
    "are",
    "the",
    "a",
    "an",
    "of",
    "to",
    "for",
    "on",
    "in",
    "with",
}

SYNONYMS = {

    "issue": [
        "problem",
        "incident",
        "bug",
        "failure",
        "error",
        "defect",
    ],

    "database": [
        "postgresql",
        "db",
        "database server",
        "sql",
    ],

    "authentication": [
        "login",
        "auth",
        "signin",
        "identity",
    ],

    "kubernetes": [
        "k8s",
        "cluster",
    ],

    "failure": [
        "error",
        "incident",
        "problem",
        "crash",
    ],

    "restart": [
        "reboot",
        "reload",
    ],

    "deployment": [
        "release",
        "rollout",
    ],

    "api": [
        "endpoint",
        "service",
    ],

    "ticket": [
        "jira",
        "issue",
    ],

    "meeting": [
        "discussion",
        "review",
    ],

    "security": [
        "authentication",
        "authorization",
    ],
}


def expand_query(query):
    """
    Enterprise Query Expansion

    Combines

    - Original query
    - Stop-word removal
    - Synonym expansion
    - Knowledge graph expansion

    Returns ONE expanded query string.
    """

    logger.info("Expanding query.")

    expanded = set()

    query = query.strip()

    expanded.add(query)

    words = query.lower().split()

    # -----------------------------
    # Remove stop words
    # -----------------------------

    keywords = [
        word
        for word in words
        if word not in STOP_WORDS
    ]

    if keywords:
        expanded.add(
            " ".join(keywords)
        )

    # -----------------------------
    # Synonyms
    # -----------------------------

    for word in words:

        if word in SYNONYMS:

            for synonym in SYNONYMS[word]:

                expanded.add(synonym)

    # -----------------------------
    # Knowledge Graph
    # -----------------------------

    matched = search_graph(query)

    for entity in matched:

        expanded.add(entity)

        for neighbor in get_neighbors(entity):

            expanded.add(str(neighbor))

    expanded_query = " ".join(expanded)

    logger.info(
        "Expanded query: %s",
        expanded_query,
    )

    return expanded_query