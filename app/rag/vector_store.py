from pathlib import Path

import faiss

from app.rag.embeddings import create_embeddings


KNOWLEDGE_DIR = Path("app/knowledge")

DEFAULT_TOP_K = 4
DEFAULT_THRESHOLD = 0.35


def load_documents() -> list[dict]:
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        content = file_path.read_text(
            encoding="utf-8"
        )

        chunks = [
            chunk.strip()
            for chunk in content.split("\n\n")
            if chunk.strip()
        ]

        for chunk_id, chunk in enumerate(chunks):
            documents.append(
                {
                    "text": chunk,
                    "source": file_path.name,
                    "chunk_id": chunk_id
                }
            )

    return documents


documents = load_documents()

if not documents:
    raise RuntimeError(
        "Knowledge base içerisinde doküman bulunamadı."
    )


document_texts = [
    document["text"]
    for document in documents
]

document_embeddings = create_embeddings(
    document_texts
)

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(document_embeddings)


def search_knowledge(
    query: str,
    top_k: int = DEFAULT_TOP_K,
    threshold: float = DEFAULT_THRESHOLD
) -> list[dict]:

    query_embedding = create_embeddings(
        [query]
    )

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(documents))
    )

    results = []

    for score, index_id in zip(
        scores[0],
        indices[0]
    ):
        if index_id == -1:
            continue

        score = float(score)

        if score < threshold:
            continue

        document = documents[index_id]

        results.append(
            {
                "text": document["text"],
                "source": document["source"],
                "chunk_id": document["chunk_id"],
                "score": round(score, 4)
            }
        )

    return results