import sqlite3
import csv
import os
import re
import time
from groq import Groq
from nexus_ai.config import GROQ_MODEL_MAIN as MODEL

client = Groq()

# In-memory DB connection reused per process
_conn = None
_loaded_file = None


def _get_conn():
    return sqlite3.connect(":memory:", check_same_thread=False)


def load_csv_to_db(filepath):
    """Load a CSV file into an in-memory SQLite table called 'data'. Returns (conn, columns)."""
    global _conn, _loaded_file

    if _loaded_file == filepath and _conn is not None:
        # already loaded
        cur = _conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        if "data" in tables:
            cur2 = _conn.execute("PRAGMA table_info(data)")
            cols = [r[1] for r in cur2.fetchall()]
            return _conn, cols

    conn = _get_conn()

    with open(filepath, newline="", encoding="utf-8-sig") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        rows = list(reader)

    if not headers or not rows:
        return None, []

    # sanitize column names for SQL
    safe_cols = [re.sub(r"[^a-zA-Z0-9_]", "_", h.strip()) for h in headers]
    col_defs = ", ".join(f'"{c}" TEXT' for c in safe_cols)
    conn.execute(f"CREATE TABLE data ({col_defs})")

    placeholders = ", ".join("?" for _ in safe_cols)
    for row in rows:
        vals = [row.get(h, "") for h in headers]
        conn.execute(f"INSERT INTO data VALUES ({placeholders})", vals)
    conn.commit()

    _conn = conn
    _loaded_file = filepath
    return conn, safe_cols


def nl_to_sql(user_question, columns, table="data"):
    """Use LLM to convert natural language question to SQL query."""
    time.sleep(1)
    system = (
        f"You convert natural language questions to SQLite SQL queries.\n"
        f"Table name: {table}\n"
        f"Columns: {', '.join(columns)}\n"
        "Rules:\n"
        "- Return ONLY the SQL query, nothing else\n"
        "- Use double quotes for column names with spaces\n"
        "- Keep queries simple and correct\n"
        "- For numeric aggregations, use CAST(col AS REAL)"
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system},
            {"role": "user", "content": user_question},
        ],
        temperature=0.1,
        max_tokens=150,
    )
    raw = resp.choices[0].message.content.strip()
    # strip markdown if present
    raw = re.sub(r"```sql|```", "", raw).strip()
    return raw


def run_sql(conn, sql):
    """Execute SQL and return results as list of dicts."""
    try:
        cur = conn.execute(sql)
        cols = [d[0] for d in cur.description] if cur.description else []
        rows = cur.fetchall()
        return [dict(zip(cols, row)) for row in rows[:50]]
    except Exception as e:
        return [{"error": str(e), "sql": sql}]


def csv_insights(filepath, task):
    """
    Full pipeline: load CSV → generate SQL questions → run queries → return insights string.
    Also answers the specific task using NL→SQL.
    """
    conn, columns = load_csv_to_db(filepath)
    if not conn:
        return "Could not load CSV file."

    row_count = conn.execute("SELECT COUNT(*) FROM data").fetchone()[0]
    insights = [f"Table loaded: {row_count} rows, columns: {', '.join(columns)}\n"]

    # Auto-generate 3 useful SQL questions based on task
    time.sleep(1)
    q_system = (
        f"Given a table with columns: {', '.join(columns)}\n"
        f"And the user task: {task}\n"
        "Write 3 useful SQL analysis questions for this data. "
        "Return as a JSON list: [\"question1\", \"question2\", \"question3\"]"
    )
    q_resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": q_system}],
        temperature=0.2,
        max_tokens=200,
    )
    raw_q = q_resp.choices[0].message.content.strip()
    import json
    questions = []
    match = re.search(r"\[.*\]", raw_q, re.DOTALL)
    if match:
        try:
            questions = json.loads(match.group())
        except Exception:
            pass
    if not questions:
        questions = [
            f"What is the total count grouped by the first column?",
            f"What are the top 5 rows ordered by the last column descending?",
        ]

    for q in questions[:3]:
        sql = nl_to_sql(q, columns)
        results = run_sql(conn, sql)
        if results and "error" not in results[0]:
            insights.append(f"Q: {q}")
            insights.append(f"SQL: {sql}")
            for r in results[:5]:
                insights.append("  " + str(r))
            insights.append("")

    return "\n".join(insights)