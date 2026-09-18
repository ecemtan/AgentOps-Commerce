from app.database.connection import get_connection


def get_order_by_id(
    order_id: str
) -> dict | None:

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                order_id,
                status,
                carrier,
                tracking_number,
                refundable
            FROM orders
            WHERE order_id = ?
            """,
            (order_id,)
        ).fetchone()

        if row is None:
            return None

        order = dict(row)

        # SQLite 0/1 değerini Python bool'a çevir.
        order["refundable"] = bool(
            order["refundable"]
        )

        return order

    finally:
        connection.close()