import duckdb
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
PAYMENTS_PATH = PROJECT_DIR / "data" / "payments.parquet"


def analyze_payment_status():
    con = duckdb.connect(database=":memory:")

    try:
        results = con.execute(
            """
            SELECT
                status,
                COUNT(*) AS payment_records,
                COUNT(DISTINCT order_id) AS distinct_orders,
                SUM(amount) AS total_recorded_amount,
                AVG(amount) AS average_recorded_amount,
                COUNT(*) FILTER (
                    WHERE amount > 0
                ) AS positive_amount_records,
                COUNT(*) FILTER (
                    WHERE amount = 0
                ) AS zero_amount_records
            FROM read_parquet(?)
            GROUP BY status
            ORDER BY payment_records DESC
            """,
            [str(PAYMENTS_PATH)],
        ).fetchdf()

        print("=" * 90)
        print("PAYMENT STATUS ANALYSIS")
        print("=" * 90)

        print(results.to_string(index=False))

        print("\n" + "=" * 90)

    finally:
        con.close()


if __name__ == "__main__":
    analyze_payment_status()