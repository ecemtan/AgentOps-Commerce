from app.repositories.order_repository import (
    get_order_by_id
)


def check_refund_eligibility(
    order_id: str
) -> dict | None:

    return get_order_by_id(
        order_id
    )