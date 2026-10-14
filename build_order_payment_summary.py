import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

ORDERS_PATH = DATA_DIR / "orders.parquet"
PAYMENTS_PATH = DATA_DIR / "payments.parquet"


def build_order_payment_summary():
    con = duckdb.connect(database=":memory:")

    try:
        summary = con.execute(
            """
            WITH payment_summary AS (
                SELECT
                    order_id,

                    COUNT(*) AS total_payment_records,

                    COUNT(*) FILTER (
                        WHERE status = 'captured'
                    ) AS captured_records,

                    COUNT(*) FILTER (
                        WHERE status = 'failed'
                    ) AS failed_records,

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
                    p.total_payment_records, 0
                ) AS total_payment_records,

                COALESCE(
                    p.captured_records, 0
                ) AS captured_records,

                COALESCE(
                    p.failed_records, 0
                ) AS failed_records,

                COALESCE(
                    p.captured_amount, 0
                ) AS captured_amount,

                COALESCE(
                    p.failed_amount, 0
                ) AS failed_amount

            FROM read_parquet(?) AS o

            LEFT JOIN payment_summary AS p
                ON o.order_id = p.order_id

            ORDER BY o.order_id
            """,
            [
                str(PAYMENTS_PATH),
                str(ORDERS_PATH),
            ],
        ).fetchdf()

        print("=" * 80)
        print("ORDER-LEVEL PAYMENT SUMMARY")
        print("=" * 80)

        print(f"Total orders: {len(summary):,}")
        print(
            "Orders without payment records:",
            int((summary["total_payment_records"] == 0).sum()),
        )
        print(
            "Orders with captured records:",
            int((summary["captured_records"] > 0).sum()),
        )
        print(
            "Orders with failed records only:",
            int(
                (
                    (summary["failed_records"] > 0)
                    & (summary["captured_records"] == 0)
                ).sum()
            ),
        )
        print(
            "Orders with both captured and failed records:",
            int(
                (
                    (summary["captured_records"] > 0)
                    & (summary["failed_records"] > 0)
                ).sum()
            ),
        )

        print("\nSample records:")
        print(summary.head(10).to_string(index=False))

        print("\n" + "=" * 80)

    finally:
        con.close()


if __name__ == "__main__":
    build_order_payment_summary()