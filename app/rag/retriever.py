from app.rag.vector_store import search_knowledge


MAX_CONTEXT_CHUNKS = 2


def retrieve_context(
    query: str,
    top_k: int = 4
) -> dict:

    results = search_knowledge(
        query=query,
        top_k=top_k
    )

    if not results:
        return {
            "context": "",
            "sources": [],
            "matches": [],
            "best_score": 0.0
        }

    # En yüksek similarity score'a sahip
    # sınırlı sayıda chunk'ı context'e al.
    selected_results = results[
        :MAX_CONTEXT_CHUNKS
    ]

    context_parts = []
    sources = []

    for result in selected_results:

        context_parts.append(
            result["text"]
        )

        if result["source"] not in sources:
            sources.append(
                result["source"]
            )

    context = "\n\n---\n\n".join(
        context_parts
    )

    return {
        "context": context,
        "sources": sources,
        "matches": selected_results,
        "best_score": results[0]["score"]
    }