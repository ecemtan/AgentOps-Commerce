from app.data.mock_db import orders


def get_order_status(order_id: str):
    return orders.get(order_id)