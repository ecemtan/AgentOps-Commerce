import re

from app.tools.product_tools import get_product


def handle_product(message: str) -> str:
    match = re.search(r"SKU-\d+", message.upper())

    if not match:
        return "Ürün kodunu paylaşır mısınız? Örnek: SKU-1001"

    product_id = match.group()

    product = get_product(product_id)

    if not product:
        return f"{product_id} kodlu ürün bulunamadı."

    stock_status = (
        f"Stokta {product['stock']} adet var."
        if product["stock"] > 0
        else "Ürün şu anda stokta yok."
    )

    return (
        f"{product['name']} - "
        f"Fiyat: {product['price']} TL. "
        f"{stock_status} "
        f"Renk: {product['color']}."
    )