"""Generate a sample SQLite database for the dashboard agent to explore.

Creates `sales.db` with a small but realistic e-commerce schema:
customers, products, orders, and order_items. Running this twice rebuilds
the database from scratch so the agent always has deterministic data.
"""

from __future__ import annotations

import random
import sqlite3
from datetime import date, timedelta
from pathlib import Path

DB_PATH = Path(__file__).parent / "sales.db"

REGIONS = ["North", "South", "East", "West"]
CATEGORIES = {
    "Electronics": ["Laptop", "Phone", "Headphones", "Monitor", "Keyboard"],
    "Home": ["Blender", "Lamp", "Cookware Set", "Vacuum", "Air Fryer"],
    "Apparel": ["T-Shirt", "Jeans", "Jacket", "Sneakers", "Hat"],
    "Books": ["Novel", "Cookbook", "Biography", "Textbook", "Comics"],
}


def build(seed: int = 42) -> Path:
    rng = random.Random(seed)

    if DB_PATH.exists():
        DB_PATH.unlink()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.executescript(
        """
        CREATE TABLE customers (
            id        INTEGER PRIMARY KEY,
            name      TEXT NOT NULL,
            region    TEXT NOT NULL,
            signup_at TEXT NOT NULL
        );

        CREATE TABLE products (
            id       INTEGER PRIMARY KEY,
            name     TEXT NOT NULL,
            category TEXT NOT NULL,
            price    REAL NOT NULL
        );

        CREATE TABLE orders (
            id          INTEGER PRIMARY KEY,
            customer_id INTEGER NOT NULL REFERENCES customers(id),
            ordered_at  TEXT NOT NULL,
            status      TEXT NOT NULL
        );

        CREATE TABLE order_items (
            id         INTEGER PRIMARY KEY,
            order_id   INTEGER NOT NULL REFERENCES orders(id),
            product_id INTEGER NOT NULL REFERENCES products(id),
            quantity   INTEGER NOT NULL,
            unit_price REAL NOT NULL
        );
        """
    )

    # Products
    products: list[tuple[int, str, str, float]] = []
    pid = 1
    for category, names in CATEGORIES.items():
        for name in names:
            price = round(rng.uniform(10, 1200), 2)
            products.append((pid, name, category, price))
            pid += 1
    cur.executemany("INSERT INTO products VALUES (?, ?, ?, ?)", products)

    # Customers
    start = date.today() - timedelta(days=365)
    customers = []
    for cid in range(1, 201):
        signup = start + timedelta(days=rng.randint(0, 300))
        customers.append(
            (cid, f"Customer {cid}", rng.choice(REGIONS), signup.isoformat())
        )
    cur.executemany("INSERT INTO customers VALUES (?, ?, ?, ?)", customers)

    # Orders + items spread across the last ~12 months
    statuses = ["completed", "completed", "completed", "shipped", "cancelled"]
    order_id = 1
    item_id = 1
    orders = []
    items = []
    for _ in range(1500):
        cust = rng.randint(1, 200)
        ordered = date.today() - timedelta(days=rng.randint(0, 364))
        status = rng.choice(statuses)
        orders.append((order_id, cust, ordered.isoformat(), status))

        for _ in range(rng.randint(1, 4)):
            prod = products[rng.randint(0, len(products) - 1)]
            qty = rng.randint(1, 5)
            items.append((item_id, order_id, prod[0], qty, prod[3]))
            item_id += 1
        order_id += 1

    cur.executemany("INSERT INTO orders VALUES (?, ?, ?, ?)", orders)
    cur.executemany("INSERT INTO order_items VALUES (?, ?, ?, ?, ?)", items)

    conn.commit()
    conn.close()
    return DB_PATH


if __name__ == "__main__":
    path = build()
    print(f"Created {path}")
