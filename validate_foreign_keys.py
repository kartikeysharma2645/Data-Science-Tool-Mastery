import duckdb
from pathlib import Path

# Project directory
PROJECT_DIR = Path(__file__).resolve().parent
DATA_DIR = PROJECT_DIR / "data"

# Foreign-key relationships: (child table, child column, parent table, parent column)
FOREIGN_KEYS = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("products", "category_id", "categories", "category_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
    ("payments", "order_id", "orders", "order_id"),
    ("returns", "order_item_id", "order_items", "order_item_id"),
    ("categories", "parent_category_id", "categories", "category_id"),
]


def validate_foreign_keys():
    """Validate foreign-key relationships across the Parquet dataset."""

    con = duckdb.connect(database=":memory:")

    try:
        print("=" * 65)
        print("FOREIGN-KEY INTEGRITY VALIDATION")
        print("=" * 65)

        total_checks = 0
        passed_checks = 0

        for child_table, child_column, parent_table, parent_column in FOREIGN_KEYS:
            child_path = DATA_DIR / f"{child_table}.parquet"
            parent_path = DATA_DIR / f"{parent_table}.parquet"

            # Ensure both dataset files exist.
            if not child_path.exists() or not parent_path.exists():
                raise FileNotFoundError(
                    f"Missing dataset file for relationship: "
                    f"{child_table}.{child_column} -> "
                    f"{parent_table}.{parent_column}"
                )

            # Count non-null foreign-key values.
            non_null_query = f"""
                SELECT COUNT(*)
                FROM read_parquet(?)
                WHERE "{child_column}" IS NOT NULL
            """

            non_null_count = con.execute(
                non_null_query, [str(child_path)]
            ).fetchone()[0]

            # Find foreign-key values with no matching parent record.
            orphan_query = f"""
                SELECT COUNT(*)
                FROM read_parquet(?) AS child
                WHERE child."{child_column}" IS NOT NULL
                  AND NOT EXISTS (
                      SELECT 1
                      FROM read_parquet(?) AS parent
                      WHERE parent."{parent_column}" = child."{child_column}"
                  )
            """

            orphan_count = con.execute(
                orphan_query,
                [str(child_path), str(parent_path)],
            ).fetchone()[0]

            total_checks += 1

            print(
                f"\n{child_table}.{child_column} -> "
                f"{parent_table}.{parent_column}"
            )
            print(f"Non-null foreign-key values: {non_null_count}")
            print(f"Orphaned foreign-key values: {orphan_count}")

            if orphan_count == 0:
                passed_checks += 1
                print("Status: PASSED")
            else:
                print("Status: FAILED")

        print("\n" + "=" * 65)
        print(f"Total relationships checked: {total_checks}")
        print(f"Passed: {passed_checks}")
        print(f"Failed: {total_checks - passed_checks}")
        print("=" * 65)

        if passed_checks == total_checks:
            print("Overall result: ALL FOREIGN-KEY CHECKS PASSED")
        else:
            print("Overall result: SOME FOREIGN-KEY CHECKS FAILED")

    finally:
        con.close()


if __name__ == "__main__":
    validate_foreign_keys()