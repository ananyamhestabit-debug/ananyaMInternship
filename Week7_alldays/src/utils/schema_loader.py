import sqlite3


def load_schema(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    tables = cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table';"
    ).fetchall()

    schema = "DATABASE TABLES:\n"

    for table in tables:
        table_name = table[0]

        columns = cursor.execute(
            f"PRAGMA table_info({table_name});"
        ).fetchall()

        col_names = [c[1] for c in columns]

        schema += f"\n{table_name}({', '.join(col_names)})\n"

    conn.close()
    return schema