from app.database.connection import get_connection


def initialize_database() -> None:

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS orders (
            order_id TEXT PRIMARY KEY,
            status TEXT NOT NULL,
            carrier TEXT,
            tracking_number TEXT,
            refundable INTEGER NOT NULL
        )
        """
    )

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS products (
            product_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            price REAL NOT NULL,
            stock INTEGER NOT NULL,
            color TEXT
        )
        """
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO orders (
            order_id,
            status,
            carrier,
            tracking_number,
            refundable
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                "ORD-1001",
                "Kargoya verildi",
                "Yurtiçi Kargo",
                "YK123456789",
                1
            ),
            (
                "ORD-1002",
                "Hazırlanıyor",
                None,
                None,
                1
            ),
            (
                "ORD-1003",
                "Teslim edildi",
                "MNG Kargo",
                "MNG987654321",
                0
            )
        ]
    )

    cursor.executemany(
        """
        INSERT OR IGNORE INTO products (
            product_id,
            name,
            price,
            stock,
            color
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        [
            (
                "SKU-1001",
                "Hydrating Face Serum",
                349.90,
                12,
                "Şeffaf"
            ),
            (
                "SKU-1002",
                "Vitamin C Serum",
                399.90,
                0,
                "Açık Sarı"
            )
        ]
    )

    connection.commit()
    connection.close()


if __name__ == "__main__":
    initialize_database()

    print(
        "AgentOps database initialized."
    )