def route_message(message: str) -> str:
    text = message.lower()

    if any(word in text for word in ["sipariş", "kargo", "teslimat"]):
        return "order"

    if any(word in text for word in ["iade", "değişim", "para iadesi"]):
        return "refund"

    if any(word in text for word in ["ürün", "stok", "fiyat", "özellik"]):
        return "product"

    return "general"