import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

ORDERS_PATH = DATA_DIR / "orders.parquet"
ORDER_ITEMS_PATH = DATA_DIR / "order_items.parquet"


def analyze_orders_without_items():
    con = duckdb.connect(database=":memory:")

    try:
        results = con.execute(
            """
            WITH item_orders AS (
                SELECT DISTINCT order_id
                FROM read_parquet(?)
            )
            SELECT
                o.status AS order_status,
                COUNT(*) AS order_count
            FROM read_parquet(?) AS o
            LEFT JOIN item_orders AS i
                ON o.order_id = i.order_id
            WHERE i.order_id IS NULL
            GROUP BY o.status
            ORDER BY order_count DESC
            """,
            [
                str(ORDER_ITEMS_PATH),
                str(ORDERS_PATH),
            ],
        ).fetchdf()

        print("=" * 65)
        print("ORDERS WITHOUT ITEM RECORDS")
        print("=" * 65)

        print(results.to_string(index=False))

        print(
            "\nTotal orders without items:",
            int(results["order_count"].sum()),
        )

        print("=" * 65)

    finally:
        con.close()


if __name__ == "__main__":
    analyze_orders_without_items()