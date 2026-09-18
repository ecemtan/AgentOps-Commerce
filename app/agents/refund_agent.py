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

from app.agents.base import (
    create_agent_result
)


def handle_refund(message: str) -> dict:

    match = re.search(
        r"ORD-\d+",
        message.upper()
    )

    # Sipariş ID yoksa iade politikası için RAG.
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
        agent_name="refund",
        tool_name="check_refund_eligibility",
        tool_function=check_refund_eligibility,
        order_id=order_id
    )

    if not tool_result["success"]:

        return create_agent_result(
            answer=(
                "İade uygunluğu kontrol edilemedi."
            ),
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
            sources=["sqlite"],
            response_type="not_found",
            metadata={
                "order_id": order_id
            }
        )

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

    return create_agent_result(
        answer=answer,
        sources=["sqlite"],
        response_type="tool",
        metadata={
            "order_id": order_id,
            "tool": "check_refund_eligibility"
        }
    )