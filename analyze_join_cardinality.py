import duckdb
from pathlib import Path

# Project paths
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

ORDERS_PATH = DATA_DIR / "orders.parquet"
ORDER_ITEMS_PATH = DATA_DIR / "order_items.parquet"
PAYMENTS_PATH = DATA_DIR / "payments.parquet"


def analyze_join_cardinality():
    """Analyze order-item and order-payment relationships."""

    # Verify that required datasets exist.
    required_files = [
        ORDERS_PATH,
        ORDER_ITEMS_PATH,
        PAYMENTS_PATH,
    ]

    for file_path in required_files:
        if not file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found: {file_path}"
            )

    con = duckdb.connect(database=":memory:")

    try:
        print("=" * 65)
        print("JOIN CARDINALITY ANALYSIS")
        print("=" * 65)

        # Count orders containing multiple items.
        multiple_items = con.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT order_id
                FROM read_parquet(?)
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ) AS item_counts
            """,
            [str(ORDER_ITEMS_PATH)],
        ).fetchone()[0]

        # Count orders with multiple payment records.
        multiple_payments = con.execute(
            """
            SELECT COUNT(*)
            FROM (
                SELECT order_id
                FROM read_parquet(?)
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ) AS payment_counts
            """,
            [str(PAYMENTS_PATH)],
        ).fetchone()[0]

        # Count orders that have both multiple items
        # and multiple payment records.
        both_multiple = con.execute(
            """
            WITH item_counts AS (
                SELECT order_id
                FROM read_parquet(?)
                GROUP BY order_id
                HAVING COUNT(*) > 1
            ),
            payment_counts AS (
                SELECT order_id
                FROM read_parquet(?)
                GROUP BY order_id
                HAVING COUNT(*) > 1
            )
            SELECT COUNT(*)
            FROM item_counts AS i
            INNER JOIN payment_counts AS p
                ON i.order_id = p.order_id
            """,
            [
                str(ORDER_ITEMS_PATH),
                str(PAYMENTS_PATH),
            ],
        ).fetchone()[0]

        print(
            "\nOrders containing multiple items:",
            multiple_items,
        )

        print(
            "Orders with multiple payment records:",
            multiple_payments,
        )

        print(
            "Orders with both multiple items "
            "and multiple payment records:",
            both_multiple,
        )

        print("\n" + "=" * 65)

    finally:
        con.close()


if __name__ == "__main__":
    analyze_join_cardinality()