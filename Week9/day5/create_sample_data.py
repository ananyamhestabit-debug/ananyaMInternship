"""
Run this once to create a sample sales.csv in the data/ folder.
Usage: python3 create_sample_data.py
"""

import os
import csv
import random
from datetime import datetime, timedelta

OUTPUT_PATH = os.path.join(os.path.dirname(__file__), "data", "sales.csv")
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

PRODUCTS     = ["Laptop", "Phone", "Tablet", "Monitor", "Keyboard", "Mouse", "Headphones", "Webcam"]
CATEGORIES   = {"Laptop": "Electronics", "Phone": "Electronics", "Tablet": "Electronics",
                "Monitor": "Electronics", "Keyboard": "Accessories", "Mouse": "Accessories",
                "Headphones": "Accessories", "Webcam": "Accessories"}
REGIONS      = ["North", "South", "East", "West"]
CHANNELS     = ["Online", "In-Store", "Phone"]
SALESREPS    = ["Alice", "Bob", "Carol", "David", "Eva"]

random.seed(42)
start_date = datetime(2023, 1, 1)

rows = []
for i in range(500):
    product  = random.choice(PRODUCTS)
    qty      = random.randint(1, 20)
    price    = round(random.uniform(20, 1500), 2)
    date     = start_date + timedelta(days=random.randint(0, 364))
    rows.append({
        "order_id":    f"ORD{1000 + i}",
        "date":        date.strftime("%Y-%m-%d"),
        "product":     product,
        "category":    CATEGORIES[product],
        "region":      random.choice(REGIONS),
        "channel":     random.choice(CHANNELS),
        "sales_rep":   random.choice(SALESREPS),
        "quantity":    qty,
        "unit_price":  price,
        "total_sales": round(qty * price, 2),
    })

with open(OUTPUT_PATH, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(rows)

print(f"Created: {OUTPUT_PATH}  ({len(rows)} rows)")
