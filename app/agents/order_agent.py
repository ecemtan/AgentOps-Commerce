import re

from app.tools.order_tools import get_order_status
from app.rag.generator import generate_rag_response

from app.security.tool_authorizer import (
    execute_authorized_tool
)


def handle_order(message: str) -> dict:

    match = re.search(
        r"ORD-\d+",
        message.upper()
    )

    if not match:
        return generate_rag_response(message)

    order_id = match.group()

    tool_result = execute_authorized_tool(
        agent_name="order",
        tool_name="get_order_status",
        tool_function=get_order_status,
        order_id=order_id
    )

    if not tool_result["success"]:
        return {
            "answer": "Sipariş bilgisi alınamadı.",
            "sources": []
        }

    order = tool_result["data"]

    if not order:
        return {
            "answer": f"{order_id} numaralı sipariş bulunamadı.",
            "sources": ["mock_db"]
        }

    if order["tracking_number"]:
        answer = (
            f"{order_id} numaralı siparişinizin durumu: "
            f"{order['status']}. "
            f"Kargo firması: {order['carrier']}. "
            f"Takip numarası: {order['tracking_number']}."
        )

    else:
        answer = (
            f"{order_id} numaralı siparişinizin durumu: "
            f"{order['status']}."
        )

    return {
        "answer": answer,
        "sources": ["mock_db"]
    }