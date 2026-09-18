import re

from app.tools.product_tools import get_product
from app.rag.generator import generate_rag_response

from app.security.tool_authorizer import (
    execute_authorized_tool
)


def handle_product(message: str) -> dict:

    match = re.search(
        r"SKU-\d+",
        message.upper()
    )

    if not match:
        return generate_rag_response(message)

    product_id = match.group()

    tool_result = execute_authorized_tool(
        agent_name="product",
        tool_name="get_product",
        tool_function=get_product,
        product_id=product_id
    )

    if not tool_result["success"]:
        return {
            "answer": "Ürün bilgisi alınamadı.",
            "sources": []
        }

    product = tool_result["data"]

    if not product:
        return {
            "answer": f"{product_id} kodlu ürün bulunamadı.",
            "sources": ["mock_db"]
        }

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

    return {
        "answer": answer,
        "sources": ["mock_db"]
    }