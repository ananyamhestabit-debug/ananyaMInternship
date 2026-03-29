import sqlite3
from src.generator.sql_generator import generate_sql

def run_sql_query(query, db_path="src/data/products.db"):

    sql = generate_sql(query)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute(sql)
    results = cursor.fetchall()

    conn.close()

    return {
        "sql": sql,
        "results": results
    }