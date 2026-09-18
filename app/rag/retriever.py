from app.rag.vector_store import search_knowledge


def retrieve_context(
    query: str,
    top_k: int = 2
) -> dict:

    results = search_knowledge(
        query=query,
        top_k=top_k
    )

    if not results:
        return {
            "context": "",
            "sources": []
        }

    context_parts = []

    sources = []

    for result in results:

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
        "sources": sources
    }