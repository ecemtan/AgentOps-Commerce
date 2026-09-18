import re

from app.tools.order_tools import get_order_status
from app.rag.generator import generate_rag_response

from app.security.tool_authorizer import (
    execute_authorized_tool
)

from app.agents.base import (
    create_agent_result
)


def handle_order(message: str) -> dict:

    match = re.search(
        r"ORD-\d+",
        message.upper()
    )

    # Sipariş ID yoksa policy / FAQ bilgisi için RAG.
    if not match:

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

    order_id = match.group()

    tool_result = execute_authorized_tool(
        agent_name="order",
        tool_name="get_order_status",
        tool_function=get_order_status,
        order_id=order_id
    )

    if not tool_result["success"]:

        return create_agent_result(
            answer="Sipariş bilgisi alınamadı.",
            response_type="tool_error",
            metadata={
                "order_id": order_id
            }
        )

    order = tool_result["data"]

    if not order:

        return create_agent_result(
            answer=(
                f"{order_id} numaralı "
                "sipariş bulunamadı."
            ),
            sources=["mock_db"],
            response_type="not_found",
            metadata={
                "order_id": order_id
            }
        )

    if order["tracking_number"]:

        answer = (
            f"{order_id} numaralı siparişinizin durumu: "
            f"{order['status']}. "
            f"Kargo firması: {order['carrier']}. "
            f"Takip numarası: "
            f"{order['tracking_number']}."
        )

    else:

        answer = (
            f"{order_id} numaralı siparişinizin durumu: "
            f"{order['status']}."
        )

    return create_agent_result(
        answer=answer,
        sources=["mock_db"],
        response_type="tool",
        metadata={
            "order_id": order_id,
            "tool": "get_order_status"
        }
    )