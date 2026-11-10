from pathlib import Path
from getpass import getpass

import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, URL


# 1. PostgreSQL connection
username = input("PostgreSQL username [postgres]: ") or "postgres"
password = getpass("PostgreSQL password: ")

connection_url = URL.create(
    "postgresql+psycopg2",
    username=username,
    password=password,
    host="localhost",
    port=5432,
    database="olist_ecommerce"
)

engine = create_engine(connection_url)


# 2. SQL queries
orders_query = """
SELECT
    DATE_TRUNC('month', order_purchase_timestamp) AS month_year,
    COUNT(order_id) AS orders_per_month
FROM orders
GROUP BY month_year
ORDER BY month_year;
"""

payments_query = """
SELECT
    DATE_TRUNC('month', o.order_purchase_timestamp) AS month_year,
    ROUND(SUM(p.payment_value), 2) AS payments_per_month
FROM orders o
JOIN order_payments p
    ON o.order_id = p.order_id
GROUP BY month_year
ORDER BY month_year;
"""

avg_payment_query = """
SELECT
    month_year,
    ROUND(AVG(costs_per_order), 2) AS avg_payment_per_order
FROM (
    SELECT
        o.order_id,
        DATE_TRUNC('month', o.order_purchase_timestamp) AS month_year,
        SUM(p.payment_value) AS costs_per_order
    FROM orders o
    JOIN order_payments p
        ON o.order_id = p.order_id
    GROUP BY o.order_id, month_year
) AS monthly_orders
GROUP BY month_year
ORDER BY month_year;
"""


# 3. Load SQL results into Pandas
orders_df = pd.read_sql_query(orders_query, engine)
payments_df = pd.read_sql_query(payments_query, engine)
avg_payment_df = pd.read_sql_query(avg_payment_query, engine)

engine.dispose()


# 4. Define project reports directory
project_root = Path(__file__).resolve().parents[1]
reports_dir = project_root / "reports"
reports_dir.mkdir(exist_ok=True)



# 7. Create monthly performance dashboard

fig, axes = plt.subplots(
    nrows=3,
    ncols=1,
    figsize=(13, 12),
    sharex=True
)

# Monthly orders
axes[0].plot(
    orders_df["month_year"],
    orders_df["orders_per_month"],
    marker="o"
)
axes[0].set_title("Monthly Orders")
axes[0].set_ylabel("Number of Orders")
axes[0].grid(True)

# Monthly payments
axes[1].plot(
    payments_df["month_year"],
    payments_df["payments_per_month"],
    marker="o"
)
axes[1].set_title("Monthly Payments")
axes[1].set_ylabel("Payment Value")
axes[1].grid(True)

# Average payment per order
axes[2].plot(
    avg_payment_df["month_year"],
    avg_payment_df["avg_payment_per_order"],
    marker="o"
)
axes[2].set_title("Average Payment per Order")
axes[2].set_ylabel("Average Payment")
axes[2].set_xlabel("Month")
axes[2].grid(True)

fig.suptitle("Olist E-Commerce: Monthly Performance", fontsize=15)

fig.autofmt_xdate()
fig.tight_layout()

fig.savefig(
    reports_dir / "monthly_performance_dashboard.png",
    dpi=150,
    bbox_inches="tight"
)

plt.show()


