
import pandas as pd
from pathlib import Path

DATA_DIR = Path("data/raw")

files = {
    "customers": "olist_customers_dataset.csv",
    "orders": "olist_orders_dataset.csv",
    "products": "olist_products_dataset.csv",
    "sellers": "olist_sellers_dataset.csv",
    "order_items": "olist_order_items_dataset.csv",
    "order_payments": "olist_order_payments_dataset.csv",
    "order_reviews": "olist_order_reviews_dataset.csv",
}

data = {}

for name, filename in files.items():
    data[name] = pd.read_csv(DATA_DIR / filename)

# 1. Check primary keys
primary_keys = {
    "customers": ["customer_id"],
    "orders": ["order_id"],
    "products": ["product_id"],
    "sellers": ["seller_id"],
    "order_items": ["order_id", "order_item_id"],
    "order_payments": ["order_id", "payment_sequential"],
    "order_reviews": ["review_id"],
}

print("PRIMARY KEY CHECK")

for table, columns in primary_keys.items():
    duplicates = data[table].duplicated(subset=columns).sum()
    print(f"{table}: {duplicates} duplicate keys")

# 2. Check foreign keys
relationships = [
    ("orders", "customer_id", "customers", "customer_id"),
    ("order_items", "order_id", "orders", "order_id"),
    ("order_items", "product_id", "products", "product_id"),
    ("order_items", "seller_id", "sellers", "seller_id"),
    ("order_payments", "order_id", "orders", "order_id"),
    ("order_reviews", "order_id", "orders", "order_id"),
]

print("\nFOREIGN KEY CHECK")

for child, child_col, parent, parent_col in relationships:
    missing = (~data[child][child_col].isin(
        data[parent][parent_col]
    )).sum()

    print(f"{child}.{child_col} -> {parent}.{parent_col}: {missing} unmatched")

# 3. Check order status distribution
print("\nORDER STATUS DISTRIBUTION")
print(data["orders"]["order_status"].value_counts())

# 4. Check review score distribution
print("\nREVIEW SCORE DISTRIBUTION")
print(data["order_reviews"]["review_score"].value_counts().sort_index())

