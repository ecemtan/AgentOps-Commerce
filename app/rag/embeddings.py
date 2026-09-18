from sentence_transformers import SentenceTransformer


MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"

embedding_model = SentenceTransformer(MODEL_NAME)


def create_embeddings(texts: list[str]):
    """
    Metin listesini embedding vektörlerine dönüştürür.
    """
    embeddings = embedding_model.encode(
        texts,
        convert_to_numpy=True,
        normalize_embeddings=True
    )

    return embeddings