import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"


def build_order_analytics():
    con = duckdb.connect(database=":memory:")

    try:
        analytics = con.execute(
            """
            WITH item_summary AS (
                SELECT
                    order_id,
                    COUNT(*) AS item_record_count,
                    SUM(quantity * unit_price) AS gross_item_value,
                    SUM(discount_amount) AS total_discount
                FROM read_parquet(?)
                GROUP BY order_id
            ),
            payment_summary AS (
                SELECT
                    order_id,
                    COUNT(*) AS payment_record_count,

                    SUM(amount) FILTER (
                        WHERE status = 'captured'
                    ) AS captured_amount,

                    SUM(amount) FILTER (
                        WHERE status = 'failed'
                    ) AS failed_amount

                FROM read_parquet(?)
                GROUP BY order_id
            )
            SELECT
                o.order_id,
                o.status AS order_status,

                COALESCE(
                    i.item_record_count, 0
                ) AS item_record_count,

                COALESCE(
                    i.gross_item_value, 0
                ) AS gross_item_value,

                COALESCE(
                    i.total_discount, 0
                ) AS total_discount,

                COALESCE(
                    i.gross_item_value - i.total_discount, 0
                ) AS item_value_after_discount,

                COALESCE(
                    p.payment_record_count, 0
                ) AS payment_record_count,

                COALESCE(
                    p.captured_amount, 0
                ) AS captured_amount,

                COALESCE(
                    p.failed_amount, 0
                ) AS failed_amount

            FROM read_parquet(?) AS o

            LEFT JOIN item_summary AS i
                ON o.order_id = i.order_id

            LEFT JOIN payment_summary AS p
                ON o.order_id = p.order_id

            ORDER BY o.order_id
            """,
            [
                str(DATA_DIR / "order_items.parquet"),
                str(DATA_DIR / "payments.parquet"),
                str(DATA_DIR / "orders.parquet"),
            ],
        ).fetchdf()

        print("=" * 90)
        print("CONSOLIDATED ORDER ANALYTICS")
        print("=" * 90)

        print(f"Total orders: {len(analytics):,}")
        print(
            "Orders with item records:",
            int((analytics["item_record_count"] > 0).sum()),
        )
        print(
            "Orders with payment records:",
            int((analytics["payment_record_count"] > 0).sum()),
        )

        print(
            "\nTotal gross item value:",
            f"{analytics['gross_item_value'].sum():,.2f}",
        )

        print(
            "Total discounts:",
            f"{analytics['total_discount'].sum():,.2f}",
        )

        print(
            "Item value after discounts:",
            f"{analytics['item_value_after_discount'].sum():,.2f}",
        )

        print(
            "Total captured payment amount:",
            f"{analytics['captured_amount'].sum():,.2f}",
        )

        print(
            "Total failed payment amount:",
            f"{analytics['failed_amount'].sum():,.2f}",
        )

        print("\nSample records:")
        print(analytics.head(10).to_string(index=False))

        print("\n" + "=" * 90)

    finally:
        con.close()


if __name__ == "__main__":
    build_order_analytics()