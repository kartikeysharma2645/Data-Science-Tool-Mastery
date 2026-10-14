# Data-Science-Tool-Mastery

A practical Data Science project demonstrating SQL analytics, DuckDB, Python, and reproducible data analysis using a real-world-style e-commerce dataset.

## Overview

This project explores an e-commerce dataset using SQL and Python to develop practical data analysis skills. It focuses on relational data, join cardinality, payment analysis, order-level metrics, and data-quality investigation.

The project emphasizes reproducible analytical workflows and careful interpretation of results.

## Tech Stack

- Python
- DuckDB
- SQL
- Pandas
- Parquet
- Git and GitHub

## Dataset

The dataset contains seven Parquet files representing the following tables:

| Table | Description |
|---|---|
| `customers` | Customer information |
| `products` | Product information |
| `categories` | Product categories |
| `orders` | Order records |
| `order_items` | Items associated with orders |
| `payments` | Payment records |
| `returns` | Product return records |

The dataset contains approximately 431,000 rows across these seven tables.

The dataset files are stored locally in the `data/` directory and excluded from Git version control.

## Project Work

### 1. Data Integrity Validation

- Validated primary-key uniqueness and null values.
- Checked foreign-key relationships across the dataset.
- Examined referential integrity using DuckDB and SQL.

### 2. SQL Join Analysis

- Investigated one-to-many relationships between orders, items, and payments.
- Examined how joining tables at different granularities can multiply rows.
- Compared direct item-value calculations with calculations performed after joining payment records.

### 3. Payment Analysis

- Summarized payment records by status.
- Examined recorded amounts and zero-amount payment records.
- Compared captured and failed payment records at the order level.

### 4. Order-Level Analytics

- Aggregated item and payment information separately before joining them to orders.
- Calculated gross item value, discounts, and payment-status amounts.
- Preserved one row per order in the consolidated order-level analysis.

### 5. Data-Quality Investigation

Investigated orders without associated order-item records.

The analysis identified:

- **90,000** total orders.
- **1,242** orders without item records.
- **1,240** affected orders with payment records.
- **2** affected orders without payment records.

Among the 1,242 affected orders:

| Order status | Number of orders |
|---|---:|
| Delivered | 919 |
| Shipped | 122 |
| Processing | 86 |
| Cancelled | 60 |
| Returned | 55 |
| **Total** | **1,242** |

Further payment analysis found that all captured and failed payment records associated with these affected orders had recorded amounts of zero.

These observations identify a potential data-quality concern. They do not establish why the item records are missing or whether the records are invalid.

## Project Structure

```text
Data-Science-Tool-Mastery/
├── data/                         # Local dataset; excluded from Git
├── sql/
│   └── ecommerce_orders.schema.sql
├── analyze_join_cardinality.py
├── analyze_join_impact.py
├── analyze_orders_without_items.py
├── analyze_payment_status.py
├── build_order_analytics.py
├── validate_foreign_keys.py
├── README.md
├── LICENSE
└── .gitignore
```

## Running the Project

### Prerequisites

- Python
- DuckDB
- Pandas

### Install Dependencies

Activate your Python environment and install the required packages:

```bash
pip install duckdb pandas
```

### Run an Analysis

From the project root, execute a script:

```bash
python analyze_join_cardinality.py
```

Other analysis scripts can be run similarly.

**Note:** The local dataset must be available in the expected `data/` directory.

## Important Analytical Considerations

- Joining order items directly with payment records can multiply item values when an order has multiple payment records.
- Aggregate item and payment data separately before joining them when calculating order-level metrics.
- A captured payment status does not necessarily imply a positive payment amount.
- Captured payment amounts should not automatically be interpreted as recognized revenue.
- Missing item records require further investigation before being classified as invalid data.

## License

This project is distributed under the MIT License. See `LICENSE` for details.