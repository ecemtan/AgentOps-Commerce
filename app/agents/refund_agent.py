import re

from app.tools.refund_tools import check_refund_eligibility


def handle_refund(message: str) -> str:
    match = re.search(r"ORD-\d+", message.upper())

    if not match:
        return "İade işlemi için sipariş numaranızı paylaşır mısınız? Örnek: ORD-1001"

    order_id = match.group()

    order = check_refund_eligibility(order_id)

    if not order:
        return f"{order_id} numaralı sipariş bulunamadı."

    if order["refundable"]:
        return f"{order_id} numaralı sipariş iade için uygundur."

    return f"{order_id} numaralı sipariş şu anda iade için uygun değildir."