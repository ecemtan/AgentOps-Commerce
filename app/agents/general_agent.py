from app.rag.generator import generate_rag_response


def handle_general(message: str) -> dict:

    greetings = [
        "merhaba",
        "selam",
        "hey",
        "günaydın",
        "iyi akşamlar"
    ]

    normalized_message = message.lower().strip()

    if any(
        greeting in normalized_message
        for greeting in greetings
    ):
        return {
            "answer": (
                "Merhaba! Size sipariş, ürün, "
                "kargo veya iade konularında "
                "yardımcı olabilirim."
            ),
            "sources": []
        }

    return generate_rag_response(message)