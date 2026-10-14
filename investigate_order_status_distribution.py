import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"


def investigate_order_status_distribution():
    con = duckdb.connect(database=":memory:")

    try:
        results = con.execute(
            """
            WITH item_orders AS (
                SELECT DISTINCT order_id
                FROM read_parquet(?)
            ),

            order_classification AS (
                SELECT
                    o.order_id,
                    o.status AS order_status,

                    CASE
                        WHEN i.order_id IS NULL
                            THEN 'Without item records'
                        ELSE 'With item records'
                    END AS item_status

                FROM read_parquet(?) AS o

                LEFT JOIN item_orders AS i
                    ON o.order_id = i.order_id
            )

            SELECT
                item_status,
                order_status,
                COUNT(*) AS order_count,

                ROUND(
                    100.0 * COUNT(*) /
                    SUM(COUNT(*)) OVER (
                        PARTITION BY item_status
                    ),
                    2
                ) AS percentage_within_item_group

            FROM order_classification

            GROUP BY
                item_status,
                order_status

            ORDER BY
                item_status,
                order_count DESC
            """,
            [
                str(DATA_DIR / "order_items.parquet"),
                str(DATA_DIR / "orders.parquet"),
            ],
        ).fetchdf()

        print("=" * 95)
        print("ORDER STATUS DISTRIBUTION BY ITEM RECORD PRESENCE")
        print("=" * 95)

        print(results.to_string(index=False))

        print("\n" + "=" * 95)

    finally:
        con.close()


if __name__ == "__main__":
    investigate_order_status_distribution()