import logging

from search.models import Chunk

from search.embeddings.embedding_generator import (
    generate_embedding,
)

from search.vectorstore.faiss_store import (
    save_index,
)

logger = logging.getLogger(__name__)


def run_embedding_pipeline(
    index_path=None
):
    """
    Generates embeddings for all chunks
    and saves them into a FAISS index.

    Args:
        index_path:
            Optional custom FAISS index path.
    """

    embeddings = []

    chunks = Chunk.objects.all().order_by(
        "id"
    )

    total = chunks.count()

    logger.info(
        "Generating embeddings for %d chunks.",
        total
    )

    for i, chunk in enumerate(chunks):

        vector = generate_embedding(
            chunk.text
        )

        embeddings.append(vector)

        if (i + 1) % 1000 == 0:

            logger.info(
                "%d/%d embeddings generated.",
                i + 1,
                total
            )

    save_index(
        embeddings,
        index_path=index_path
    )

    logger.info(
        "Embedding pipeline completed."
    )

    return len(embeddings)