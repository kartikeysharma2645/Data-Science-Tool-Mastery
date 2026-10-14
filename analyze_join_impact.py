import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

ORDER_ITEMS_PATH = DATA_DIR / "order_items.parquet"
PAYMENTS_PATH = DATA_DIR / "payments.parquet"


def analyze_join_impact():
    con = duckdb.connect(database=":memory:")

    try:
        result = con.execute(
            """
            WITH item_totals AS (
                SELECT
                    order_id,
                    SUM(quantity * unit_price) AS item_value
                FROM read_parquet(?)
                GROUP BY order_id
            ),
            payment_counts AS (
                SELECT
                    order_id,
                    COUNT(*) AS payment_count
                FROM read_parquet(?)
                GROUP BY order_id
            ),
            matched_orders AS (
                SELECT
                    i.order_id,
                    i.item_value,
                    COALESCE(p.payment_count, 0) AS payment_count
                FROM item_totals AS i
                LEFT JOIN payment_counts AS p
                    ON i.order_id = p.order_id
            )
            SELECT
                SUM(item_value) AS direct_item_value,

                SUM(item_value) FILTER (
                    WHERE payment_count > 0
                ) AS matched_item_value,

                SUM(item_value * payment_count) FILTER (
                    WHERE payment_count > 0
                ) AS joined_item_value,

                SUM(item_value * (payment_count - 1)) FILTER (
                    WHERE payment_count > 1
                ) AS multiplication_increase,

                SUM(item_value) FILTER (
                    WHERE payment_count = 0
                ) AS unmatched_item_value

            FROM matched_orders
            """,
            [
                str(ORDER_ITEMS_PATH),
                str(PAYMENTS_PATH),
            ],
        ).fetchone()

        (
            direct_value,
            matched_value,
            joined_value,
            multiplication_increase,
            unmatched_value,
        ) = result

        print("=" * 65)
        print("JOIN MULTIPLICATION IMPACT")
        print("=" * 65)

        print(f"Direct gross item value: {direct_value:,.2f}")
        print(f"Value for orders with payments: {matched_value:,.2f}")
        print(f"Value for orders without payments: {unmatched_value:,.2f}")
        print(f"Joined gross item value: {joined_value:,.2f}")
        print(
            f"Increase caused by multiple payment records: "
            f"{multiplication_increase:,.2f}"
        )

        print("\nVerification:")
        print(
            f"Matched value + multiplication increase: "
            f"{matched_value + multiplication_increase:,.2f}"
        )

        print("\n" + "=" * 65)

    finally:
        con.close()


if __name__ == "__main__":
    analyze_join_impact()