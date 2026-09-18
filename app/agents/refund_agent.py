import re

from app.tools.refund_tools import (
    check_refund_eligibility
)

from app.rag.generator import (
    generate_rag_response
)

from app.security.tool_authorizer import (
    execute_authorized_tool
)


def handle_refund(message: str) -> dict:

    match = re.search(
        r"ORD-\d+",
        message.upper()
    )

    if not match:
        return generate_rag_response(message)

    order_id = match.group()

    tool_result = execute_authorized_tool(
        agent_name="refund",
        tool_name="check_refund_eligibility",
        tool_function=check_refund_eligibility,
        order_id=order_id
    )

    if not tool_result["success"]:
        return {
            "answer": "İade uygunluğu kontrol edilemedi.",
            "sources": []
        }

    order = tool_result["data"]

    if not order:
        return {
            "answer": f"{order_id} numaralı sipariş bulunamadı.",
            "sources": ["mock_db"]
        }

    if order["refundable"]:
        answer = (
            f"{order_id} numaralı sipariş "
            "iade için uygundur."
        )

    else:
        answer = (
            f"{order_id} numaralı sipariş "
            "iade için uygun değildir."
        )

    return {
        "answer": answer,
        "sources": ["mock_db"]
    }