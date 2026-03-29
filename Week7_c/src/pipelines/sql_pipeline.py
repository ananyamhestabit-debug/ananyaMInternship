import sqlite3
from src.generator.sql_generator import generate_sql


DB_PATH = "src/data/products.db"


def run_sql_query(query):

    # 🔹 Generate SQL from NL query
    sql = generate_sql(query)

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute(sql)
        results = cursor.fetchall()

        conn.close()

        # NO FALLBACK (IMPORTANT)
        if len(results) == 0:
            return {
                "sql": sql,
                "results": []
            }

        return {
            "sql": sql,
            "results": results
        }

    except Exception as e:
        return {
            "sql": sql,
            "error": str(e),
            "results": []
        }