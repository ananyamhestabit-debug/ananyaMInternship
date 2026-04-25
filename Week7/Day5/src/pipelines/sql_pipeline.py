import sqlite3
import re
from generator.sql_generator import generate_sql
from utils.schema_loader import load_schema

DB_PATH = "database/sample.db"


# -------- GET VALID TABLES --------
def get_tables(schema):
    tables = []
    for line in schema.split("\n"):
        if line.startswith("Table:"):
            tables.append(line.replace("Table:", "").strip())
    return tables


# -------- FIX QUERY --------
def fix_query(query, schema):
    tables = get_tables(schema)
    q = query.lower()

    # check if valid table exists
    valid = any(f"from {t.lower()}" in q for t in tables)

    if not valid and tables:
        # replace incorrect table
        query = re.sub(r"from\s+\w+", f"FROM {tables[0]}", query, flags=re.IGNORECASE)

    return query


# -------- EXECUTE QUERY --------
def execute_query(query):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    try:
        cur.execute(query)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description]
        return cols, rows
    except Exception as e:
        return None, str(e)
    finally:
        conn.close()


# -------- MAIN PIPELINE --------
def run_sql_pipeline(question):
    schema = load_schema(DB_PATH)

    # STEP 1: generate SQL
    query = generate_sql(question, schema)

    # STEP 2: fix schema issues
    query = fix_query(query, schema)

    # STEP 3: execute
    columns, rows = execute_query(query)

    # STEP 4: retry if failed
    if columns is None:
        print("Retrying SQL generation...")

        query = generate_sql(question + " use correct table names", schema)
        query = fix_query(query, schema)

        columns, rows = execute_query(query)

    # STEP 5: final fallback
    if columns is None:
        return {
            "error": rows,
            "sql": query
        }

    return {
        "sql": query,
        "columns": columns,
        "rows": rows
    }


# -------- CLI TEST --------
if __name__ == "__main__":
    print("SQL CLI Mode Started\n")

    while True:
        q = input("Enter your SQL question (type exit to quit): ")

        if q.lower() == "exit":
            break

        result = run_sql_pipeline(q)

        if "error" in result:
            print("\nError:\n", result["error"])
            print("\nSQL:\n", result["sql"])
        else:
            print("\nSQL:\n", result["sql"])
            print("\nResults:\n")

            for row in result["rows"]:
                print(", ".join(map(str, row)))

        print("\n" + "=" * 50 + "\n")