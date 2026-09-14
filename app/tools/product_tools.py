from app.data.mock_db import products


def get_product(product_id: str):
    return products.get(product_id)