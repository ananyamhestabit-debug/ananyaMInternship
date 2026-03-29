import sqlite3

def load_schema(db_path="src/data/products.db"):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(products);")
    columns = cursor.fetchall()

    conn.close()

    return [col[1] for col in columns]