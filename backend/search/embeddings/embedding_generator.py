from sentence_transformers import SentenceTransformer


# Load model once
model = SentenceTransformer(
    "BAAI/bge-small-en-v1.5"
)


def generate_embedding(text):

    embedding = model.encode(
        text,
        normalize_embeddings=True
    )

    return embedding.tolist()