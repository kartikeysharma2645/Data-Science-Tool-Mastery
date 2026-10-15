# Data-Science-Tool-Mastery

A practical Data Science project demonstrating SQL analytics, DuckDB, Python, interactive data analysis, visualization, and reproducible analytical workflows using a synthetic e-commerce dataset.

## Overview

This project explores an e-commerce dataset using SQL and Python to develop practical data analysis skills.

It covers relational data, join cardinality, payment analysis, order-level metrics, data-quality investigation, customer demographics, product pricing, and data visualization.

The project emphasizes reproducible analytical workflows, data integrity, and careful interpretation of results.

## Tech Stack

- Python
- DuckDB
- SQL
- Pandas
- Matplotlib
- Seaborn
- Jupyter Notebook
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

The dataset contains 431,024 rows across these seven tables.

The dataset files are stored locally in the `data/` directory and excluded from Git version control.

The dataset is synthetic and is used for analytical practice.

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

### 6. Customer Analysis and Visualization

Analyzed customer geography, loyalty tiers, marketing preferences, and signup trends using DuckDB, Pandas, Matplotlib, and Seaborn.

Key findings:

- The dataset contains **12,000 customers across 17 countries**.
- The United States has the largest customer base, with **2,075 customers (17.29%)**.
- **5,296 customers (44.13%)** have no recorded loyalty tier.
- Bronze is the most common recorded loyalty tier, with **4,023 customers**.
- **7,489 customers (62.41%)** opted in to marketing communications.
- Customer signups totalled 4,022 in 2023, 4,059 in 2024, and 3,919 in 2025.
- November and December consistently recorded higher signup counts than most other months across the three years examined.

The repeated year-end signup increases suggest a possible seasonal pattern, but the analysis does not establish their cause.

### 7. Product Analysis and Visualization

Analyzed product categories, listed prices, unit costs, unit margins, and recorded discontinuation dates.

Key findings:

- The catalog contains **2,000 products across 24 categories**.
- All 24 categories contain at least one product.
- Garden Tools has the largest catalog, with **102 products**.
- Sprinklers has the highest average listed product price, at **38.26**.
- Sprinklers also has the highest average unit margin, at **16.04**.
- The Classic Terracotta Sprinkler has a unit margin of **114.95**.
- Product prices show a right-skewed distribution, with most products concentrated in lower price ranges.
- **153 products (7.65%)** have a recorded discontinuation date.

Unit margin is calculated as listed unit price minus unit cost. It does not represent total profit or realized profitability.

## Interactive Analysis Notebook

The customer and product analyses are documented in:

`notebooks/ecommerce_customer_product_analysis.ipynb`

The notebook uses DuckDB to query the Parquet data and Pandas, Matplotlib, and Seaborn to analyze and visualize the results.

It includes data previews, missing-value checks, SQL aggregations, summary tables, visualizations, and analytical findings.

## Project Structure

```text
Data-Science-Tool-Mastery/
├── data/                                  # Local dataset; excluded from Git
├── sql/
│   └── ecommerce_orders.schema.sql
├── notebooks/
│   └── ecommerce_customer_product_analysis.ipynb
├── analyze_join_cardinality.py
├── analyze_join_impact.py
├── analyze_orders_without_items.py
├── analyze_payment_status.py
├── build_order_analytics.py
├── build_order_payment_summary.py
├── investigate_missing_items_amounts.py
├── investigate_missing_items_financial_impact.py
├── investigate_order_status_distribution.py
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
- Matplotlib
- Seaborn
- JupyterLab

### Install Dependencies

Activate your Python environment and install the required packages:

```bash
python -m pip install duckdb pandas matplotlib seaborn jupyterlab
```

### Run a Python Analysis Script

From the project root, execute a script:

```bash
python analyze_join_cardinality.py
```

Other analysis scripts can be run similarly.

### Run the Interactive Notebook

Launch JupyterLab:

```bash
python -m jupyter lab
```

Open `notebooks/ecommerce_customer_product_analysis.ipynb` and run the notebook cells from top to bottom.

### Dataset Requirement

The Parquet files must be available locally in the expected `data/` directory. The dataset is excluded from Git version control, so it must be obtained separately before running the analyses.

## Important Analytical Considerations

- Joining order items directly with payment records can multiply item values when an order has multiple payment records.
- Aggregate item and payment data separately before joining them when calculating order-level metrics.
- A captured payment status does not necessarily imply a positive payment amount.
- Captured payment amounts should not automatically be interpreted as recognized revenue.
- Missing item records require further investigation before being classified as invalid data.
- Missing loyalty tiers may affect conclusions about loyalty-program membership.
- Customer signup patterns do not establish the causes of year-end increases.
- Product-level margins do not account for sales volume, discounts, returns, shipping, or operating expenses.
- Missing discontinuation dates do not definitively establish that products remain available for sale.

## License

This project is distributed under the MIT License. See `LICENSE` for details.