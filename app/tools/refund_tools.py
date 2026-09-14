from app.data.mock_db import orders


def check_refund_eligibility(order_id: str):
    return orders.get(order_id)