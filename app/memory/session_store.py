import re


# Şimdilik memory RAM'de tutulacak.
# Daha sonra SQLite/Redis'e taşıyacağız.
sessions: dict[str, dict] = {}


def get_session(session_id: str) -> dict:
    if session_id not in sessions:
        sessions[session_id] = {
            "messages": [],
            "last_order_id": None,
            "last_product_id": None
        }

    return sessions[session_id]


def update_session(
    session_id: str,
    user_message: str,
    assistant_response: str
) -> None:

    session = get_session(session_id)

    session["messages"].append(
        {
            "role": "user",
            "content": user_message
        }
    )

    session["messages"].append(
        {
            "role": "assistant",
            "content": assistant_response
        }
    )

    # Mesajda ORD varsa hatırla.
    order_match = re.search(
        r"ORD-\d+",
        user_message.upper()
    )

    if order_match:
        session["last_order_id"] = order_match.group()

    # Mesajda SKU varsa hatırla.
    product_match = re.search(
        r"SKU-\d+",
        user_message.upper()
    )

    if product_match:
        session["last_product_id"] = product_match.group()


def enrich_message_with_memory(
    session_id: str,
    message: str
) -> str:

    session = get_session(session_id)

    message_lower = message.lower()

    # Follow-up iade/sipariş sorusunda önceki ORD'yi ekle.
    order_follow_up_words = [
        "iade",
        "geri gönder",
        "geri gonder",
        "nerede",
        "kargo",
        "sipariş",
        "siparis",
        "bunu",
        "onu"
    ]

    if (
        session["last_order_id"]
        and "ORD-" not in message.upper()
        and any(
            word in message_lower
            for word in order_follow_up_words
        )
    ):
        return (
            f"{message} "
            f"[Önceki sipariş: {session['last_order_id']}]"
        )

    # Follow-up ürün sorusunda önceki SKU'yu ekle.
    product_follow_up_words = [
        "stok",
        "fiyat",
        "ürün",
        "urun",
        "bunu",
        "onu"
    ]

    if (
        session["last_product_id"]
        and "SKU-" not in message.upper()
        and any(
            word in message_lower
            for word in product_follow_up_words
        )
    ):
        return (
            f"{message} "
            f"[Önceki ürün: {session['last_product_id']}]"
        )

    return message