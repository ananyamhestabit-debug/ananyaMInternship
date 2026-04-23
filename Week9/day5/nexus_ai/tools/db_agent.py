import sqlite3
import os

# Always resolve DB path relative to nexus_ai/data/
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB = os.path.join(BASE_DIR, "data", "sales.db")


def create_table_from_csv(data):
    if not data:
        raise ValueError("CSV file is empty or not loaded correctly")
    os.makedirs(os.path.dirname(DB), exist_ok=True)
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS sales")
    columns = data[0].keys()
    col_str = ", ".join([f'"{c}" TEXT' for c in columns])
    cur.execute(f"CREATE TABLE sales ({col_str})")
    for row in data:
        cur.execute(
            f"INSERT INTO sales VALUES ({','.join(['?'] * len(row))})",
            list(row.values())
        )
    conn.commit()
    conn.close()
    print(f"[DB] Table 'sales' created with {len(data)} rows.")


def get_schema():
    conn = sqlite3.connect(DB)
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(sales)")
    columns = [col[1] for col in cur.fetchall()]
    conn.close()
    return columns


def run_sql(sql_query: str):
    """Run a raw SQL SELECT query and return results."""
    if not sql_query.lower().strip().startswith("select"):
        return "Only SELECT queries are allowed"
    try:
        conn = sqlite3.connect(DB)
        cur = conn.cursor()
        cur.execute(sql_query)
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description] if cur.description else []
        conn.close()
        return {"columns": col_names, "rows": rows} if rows else "No results found."
    except Exception as e:
        return f"DB Error: {e}"
