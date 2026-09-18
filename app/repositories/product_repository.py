from app.database.connection import get_connection


def get_product_by_id(
    product_id: str
) -> dict | None:

    connection = get_connection()

    try:
        row = connection.execute(
            """
            SELECT
                product_id,
                name,
                price,
                stock,
                color
            FROM products
            WHERE product_id = ?
            """,
            (product_id,)
        ).fetchone()

        if row is None:
            return None

        return dict(row)

    finally:
        connection.close()