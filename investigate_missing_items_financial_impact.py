import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"


def investigate_financial_impact():
    con = duckdb.connect(database=":memory:")

    try:
        results = con.execute(
            """
            WITH item_orders AS (
                SELECT DISTINCT order_id
                FROM read_parquet(?)
            ),

            order_item_status AS (
                SELECT
                    o.order_id,
                    CASE
                        WHEN i.order_id IS NULL
                            THEN 'Without item records'
                        ELSE 'With item records'
                    END AS item_status
                FROM read_parquet(?) AS o
                LEFT JOIN item_orders AS i
                    ON o.order_id = i.order_id
            ),

            payment_summary AS (
                SELECT
                    order_id,

                    COUNT(*) AS payment_record_count,

                    COUNT(*) FILTER (
                        WHERE status = 'captured'
                    ) AS captured_record_count,

                    SUM(amount) FILTER (
                        WHERE status = 'captured'
                    ) AS captured_amount

                FROM read_parquet(?)
                GROUP BY order_id
            )

            SELECT
                o.item_status,

                COUNT(*) AS total_orders,

                COUNT(*) FILTER (
                    WHERE COALESCE(p.payment_record_count, 0) > 0
                ) AS orders_with_payment_records,

                COUNT(*) FILTER (
                    WHERE COALESCE(p.captured_record_count, 0) > 0
                ) AS orders_with_captured_records,

                COALESCE(
                    SUM(p.captured_amount),
                    0
                ) AS total_captured_amount

            FROM order_item_status AS o

            LEFT JOIN payment_summary AS p
                ON o.order_id = p.order_id

            GROUP BY o.item_status

            ORDER BY o.item_status
            """,
            [
                str(DATA_DIR / "order_items.parquet"),
                str(DATA_DIR / "orders.parquet"),
                str(DATA_DIR / "payments.parquet"),
            ],
        ).fetchdf()

        print("=" * 95)
        print("FINANCIAL IMPACT: ORDERS WITH AND WITHOUT ITEM RECORDS")
        print("=" * 95)

        print(results.to_string(index=False))

        print("\n" + "=" * 95)
        print(
            "Note: Captured payment amounts are not necessarily "
            "equivalent to recognized revenue."
        )
        print("=" * 95)

    finally:
        con.close()


if __name__ == "__main__":
    investigate_financial_impact()