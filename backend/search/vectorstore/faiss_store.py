import logging
from pathlib import Path

import faiss
import numpy as np

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[3]

DEFAULT_INDEX_PATH = BASE_DIR / "vector_store.index"
INDEX_PATH = BASE_DIR / "vector_store.index"

def save_index(
    embeddings,
    index_path=DEFAULT_INDEX_PATH
):
    """
    Saves embeddings into a FAISS index.

    Args:
        embeddings:
            List of embedding vectors.

        index_path:
            Location where the FAISS index
            should be saved.
    """

    # ----------------------------
    # Nothing to save
    # ----------------------------
    if index_path is None:
        index_path = DEFAULT_INDEX_PATH 
    if len(embeddings) == 0:

        logger.warning(
            "No embeddings found. "
            "Skipping FAISS index creation."
        )

        return

    # ----------------------------
    # Convert to NumPy
    # ----------------------------

    vectors = np.array(
        embeddings,
        dtype=np.float32
    )

    # ----------------------------
    # Create FAISS index
    # ----------------------------

    dimension = vectors.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )
    print(vectors.shape)
    index.add(vectors)

    # ----------------------------
    # Save index
    # ----------------------------

    faiss.write_index(
        index,
        str(index_path)
    )

    logger.info(
        "Saved %d vectors to %s",
        index.ntotal,
        index_path
    )


def load_index(index_path=None):
    """
    Loads a FAISS index.

    Args:
        index_path:
            Optional custom path.
            Used mainly in tests.

    Returns:
        FAISS Index
    """

    # ----------------------------
    # Use default path
    # ----------------------------

    if index_path is None:
        index_path = INDEX_PATH

    logger.info(
        "Loading FAISS index from %s",
        index_path
    )

    return faiss.read_index(
        str(index_path)
    )