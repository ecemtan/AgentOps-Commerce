from app.rag.generator import (
    generate_rag_response
)

from app.agents.base import (
    create_agent_result
)


def handle_general(message: str) -> dict:

    greetings = [
        "merhaba",
        "selam",
        "hey",
        "günaydın",
        "iyi akşamlar"
    ]

    normalized_message = (
        message.lower().strip()
    )

    if any(
        greeting in normalized_message
        for greeting in greetings
    ):

        return create_agent_result(
            answer=(
                "Merhaba! Size sipariş, ürün, "
                "kargo veya iade konularında "
                "yardımcı olabilirim."
            ),
            response_type="deterministic"
        )

    rag_result = generate_rag_response(
        message
    )

    return create_agent_result(
        answer=rag_result["answer"],
        sources=rag_result["sources"],
        response_type="rag",
        metadata={
            "rag": rag_result.get("rag", {})
        }
    )