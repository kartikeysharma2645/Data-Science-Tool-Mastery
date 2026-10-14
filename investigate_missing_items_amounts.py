import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"


def investigate_missing_item_amounts():
    con = duckdb.connect(database=":memory:")

    try:
        results = con.execute(
            """
            WITH item_orders AS (
                SELECT DISTINCT order_id
                FROM read_parquet(?)
            ),

            missing_item_orders AS (
                SELECT o.order_id
                FROM read_parquet(?) AS o
                LEFT JOIN item_orders AS i
                    ON o.order_id = i.order_id
                WHERE i.order_id IS NULL
            )

            SELECT
                p.status AS payment_status,
                COUNT(*) AS payment_records,
                COUNT(DISTINCT p.order_id) AS distinct_orders,
                SUM(p.amount) AS total_amount,
                MIN(p.amount) AS minimum_amount,
                MAX(p.amount) AS maximum_amount,
                COUNT(*) FILTER (
                    WHERE p.amount = 0
                ) AS zero_amount_records,
                COUNT(*) FILTER (
                    WHERE p.amount > 0
                ) AS positive_amount_records

            FROM read_parquet(?) AS p

            INNER JOIN missing_item_orders AS m
                ON p.order_id = m.order_id

            GROUP BY p.status
            ORDER BY p.status
            """,
            [
                str(DATA_DIR / "order_items.parquet"),
                str(DATA_DIR / "orders.parquet"),
                str(DATA_DIR / "payments.parquet"),
            ],
        ).fetchdf()

        print("=" * 90)
        print("PAYMENT AMOUNTS FOR ORDERS WITHOUT ITEM RECORDS")
        print("=" * 90)
        print(results.to_string(index=False))
        print("=" * 90)

    finally:
        con.close()


if __name__ == "__main__":
    investigate_missing_item_amounts()