import sqlite3
from generator.sql_generator import generate_sql, validate_sql
from utils.schema_loader import load_schema

DB_PATH = "database/sample.db"


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


def summarize_result(columns, rows):
    if not rows:
        return "No results found."

    result = ""
    for row in rows:
        result += ", ".join(str(x) for x in row) + "\n"

    return result


def run_sql_pipeline(question):
    schema = load_schema(DB_PATH)

    sql_query = generate_sql(question, schema)

    if not validate_sql(sql_query):
        return {
            "error": "Unsafe SQL detected",
            "sql": sql_query
        }

    columns, rows = execute_query(sql_query)

    if columns is None:
        return {
            "error": rows,
            "sql": sql_query
        }

    summary = summarize_result(columns, rows)

    return {
        "sql": sql_query,
        "columns": columns,
        "rows": rows,
        "summary": summary
    }


#cli 
def pretty_print(result):
    print("\nGenerated SQL:\n")
    print(result["sql"])

    print("\nResults:\n")
    for row in result["rows"]:
        print(", ".join(str(x) for x in row))

    print("\nSummary:\n")
    print(result["summary"])



if __name__ == "__main__":
    print("SQL CLI Mode Started\n")

    while True:
        q = input("Enter your SQL question (type 'exit' to quit): ")

        if q.lower() == "exit":
            break

        result = run_sql_pipeline(q)

        if "error" in result:
            print("\nError:\n")
            print(result["error"])
            print("\nGenerated SQL:\n")
            print(result["sql"])
        else:
            pretty_print(result)

        print("\n" + "="*50 + "\n")