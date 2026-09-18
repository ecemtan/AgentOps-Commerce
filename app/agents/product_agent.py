import re

from app.tools.product_tools import get_product
from app.rag.generator import generate_rag_response

from app.security.tool_authorizer import (
    execute_authorized_tool
)

from app.agents.base import (
    create_agent_result
)


def handle_product(message: str) -> dict:

    match = re.search(
        r"SKU-\d+",
        message.upper()
    )

    # SKU yoksa ürün knowledge base'i için RAG.
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

    product_id = match.group()

    tool_result = execute_authorized_tool(
        agent_name="product",
        tool_name="get_product",
        tool_function=get_product,
        product_id=product_id
    )

    if not tool_result["success"]:

        return create_agent_result(
            answer="Ürün bilgisi alınamadı.",
            response_type="tool_error",
            metadata={
                "product_id": product_id
            }
        )

    product = tool_result["data"]

    if not product:

        return create_agent_result(
            answer=(
                f"{product_id} kodlu ürün bulunamadı."
            ),
            sources=["sqlite"],
            response_type="not_found",
            metadata={
                "product_id": product_id
            }
        )

    if product["stock"] > 0:

        stock_status = (
            f"Stokta {product['stock']} adet var."
        )

    else:

        stock_status = (
            "Ürün şu anda stokta yok."
        )

    answer = (
        f"{product['name']} - "
        f"Fiyat: {product['price']} TL. "
        f"{stock_status} "
        f"Renk: {product['color']}."
    )

    return create_agent_result(
        answer=answer,
        sources=["sqlite"],
        response_type="tool",
        metadata={
            "product_id": product_id,
            "tool": "get_product"
        }
    )