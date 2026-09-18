from pathlib import Path

import faiss

from app.rag.embeddings import create_embeddings


KNOWLEDGE_DIR = Path("app/knowledge")


def load_documents() -> list[dict]:
    documents = []

    for file_path in KNOWLEDGE_DIR.glob("*.txt"):
        content = file_path.read_text(encoding="utf-8")

        chunks = [
            chunk.strip()
            for chunk in content.split("\n\n")
            if chunk.strip()
        ]

        for chunk in chunks:
            documents.append(
                {
                    "text": chunk,
                    "source": file_path.name
                }
            )

    return documents


documents = load_documents()


if not documents:
    raise RuntimeError("Knowledge base içerisinde doküman bulunamadı.")


document_texts = [
    document["text"]
    for document in documents
]


document_embeddings = create_embeddings(document_texts)

dimension = document_embeddings.shape[1]

index = faiss.IndexFlatIP(dimension)

index.add(document_embeddings)


def search_knowledge(
    query: str,
    top_k: int = 3,
    threshold: float = 0.45
) -> list[dict]:

    query_embedding = create_embeddings([query])

    scores, indices = index.search(
        query_embedding,
        min(top_k, len(documents))
    )

    results = []

    for score, index_id in zip(scores[0], indices[0]):

        if index_id == -1:
            continue

        if float(score) < threshold:
            continue

        document = documents[index_id]

        results.append(
            {
                "text": document["text"],
                "source": document["source"],
                "score": float(score)
            }
        )

    return results