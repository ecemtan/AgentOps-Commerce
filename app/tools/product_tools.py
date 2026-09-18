from app.repositories.product_repository import (
    get_product_by_id
)


def get_product(
    product_id: str
) -> dict | None:

    return get_product_by_id(
        product_id
    )