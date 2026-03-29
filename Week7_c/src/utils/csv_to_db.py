import pandas as pd
import sqlite3

def csv_to_sqlite(
    csv_path="src/data/raw/products-1000.csv",
    db_path="src/data/products.db",
    table_name="products"
):
    df = pd.read_csv(csv_path)

    conn = sqlite3.connect(db_path)
    df.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

    return f"{table_name} table created successfully"