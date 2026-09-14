import re

from app.tools.order_tools import get_order_status


def handle_order(message: str) -> str:
    match = re.search(r"ORD-\d+", message.upper())

    if not match:
        return "Sipariş numaranızı paylaşır mısınız? Örnek: ORD-1001"

    order_id = match.group()

    order = get_order_status(order_id)

    if not order:
        return f"{order_id} numaralı sipariş bulunamadı."

    if order["tracking_number"]:
        return (
            f"{order_id} numaralı siparişinizin durumu: {order['status']}. "
            f"Kargo firması: {order['carrier']}. "
            f"Takip numarası: {order['tracking_number']}."
        )

    return (
        f"{order_id} numaralı siparişinizin durumu: "
        f"{order['status']}."
    )