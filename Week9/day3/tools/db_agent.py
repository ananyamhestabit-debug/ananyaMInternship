"""
DAY 3 — DB Agent
Tool: SQLite database — create, insert, query
"""

import sqlite3
import csv
import os
import time
import re
from groq import Groq

client = Groq()

DB_PATH = "data/sales.db"

DB_AGENT_PROMPT = """You are the DB Agent in a multi-agent AI system.

Your ONLY job: Write and execute SQL queries on a SQLite database.

The database has a table called `sales` with these columns:
- date (TEXT)
- product (TEXT)
- category (TEXT)
- quantity (INTEGER)
- price (REAL)
- revenue (REAL)
- region (TEXT)

Given an instruction, write the correct SQL query to answer it.

Return ONLY a SQL code block like this:
```sql
SELECT ...
```

No explanation. Just the SQL."""


def init_db_from_csv(csv_path: str = "data/sales.csv", db_path: str = DB_PATH):
    """Creates SQLite DB and loads CSV data into it"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sales (
            date TEXT,
            product TEXT,
            category TEXT,
            quantity INTEGER,
            price REAL,
            revenue REAL,
            region TEXT
        )
    """)

    # Clear existing data
    cursor.execute("DELETE FROM sales")

    # Load from CSV
    if os.path.exists(csv_path):
        with open(csv_path, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                cursor.execute("""
                    INSERT INTO sales VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    row["date"], row["product"], row["category"],
                    int(row["quantity"]), float(row["price"]),
                    float(row["revenue"]), row["region"]
                ))

    conn.commit()
    row_count = cursor.execute("SELECT COUNT(*) FROM sales").fetchone()[0]
    conn.close()
    print(f"[DB AGENT] Database initialized: {row_count} rows loaded into `sales` table")
    return row_count


def execute_sql(query: str, db_path: str = DB_PATH) -> dict:
    """Executes a SQL query and returns results"""
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        conn.close()

        results = [dict(row) for row in rows]
        return {"success": True, "columns": columns, "rows": results, "count": len(results)}

    except Exception as e:
        return {"success": False, "error": str(e), "rows": [], "columns": []}


def format_results(query_result: dict) -> str:
    """Formats SQL results as readable table"""
    if not query_result["success"]:
        return f"❌ SQL Error: {query_result['error']}"

    rows = query_result["rows"]
    if not rows:
        return "📊 Query returned 0 results"

    cols = query_result["columns"]
    output = f"📊 DB QUERY RESULTS ({query_result['count']} rows):\n\n"

    # Header
    output += " | ".join(f"{c:<20}" for c in cols) + "\n"
    output += "-" * (23 * len(cols)) + "\n"

    # Rows
    for row in rows[:20]:
        output += " | ".join(f"{str(row.get(c,'')):<20}" for c in cols) + "\n"

    if query_result["count"] > 20:
        output += f"... and {query_result['count'] - 20} more rows\n"

    return output


def extract_sql(text: str) -> str:
    """Extracts SQL from markdown code block"""
    match = re.search(r'```sql\n(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    return text.strip()


def run_db_agent(instruction: str) -> dict:
    """
    Generates SQL for the instruction, executes it on SQLite,
    returns formatted results.
    """
    print(f"\n[DB AGENT] Instruction: {instruction[:80]}...")

    # Ensure DB exists
    if not os.path.exists(DB_PATH):
        init_db_from_csv()

    time.sleep(2)  # rate limit buffer

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": DB_AGENT_PROMPT},
            {"role": "user", "content": instruction}
        ],
        temperature=0.2,
        max_tokens=400
    )

    raw = response.choices[0].message.content.strip()
    sql = extract_sql(raw)

    print(f"[DB AGENT] Generated SQL: {sql[:100]}...")

    result = execute_sql(sql)
    formatted = format_results(result)

    print(f"[DB AGENT] Query complete ✓ ({result.get('count', 0)} rows)")

    output = f"🗄️ SQL QUERY:\n```sql\n{sql}\n```\n\n{formatted}"

    return {
        "agent": "db_agent",
        "instruction": instruction,
        "sql": sql,
        "result": result,
        "output": output
    }


if __name__ == "__main__":
    init_db_from_csv()
    result = run_db_agent("Show top 5 products by total revenue")
    print(result["output"])
