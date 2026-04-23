import sqlite3
import json
import time
from nexus_ai.config import DB_PATH


# --- Short-term session memory ---

class SessionMemory:
    def __init__(self, max_turns=20):
        self.turns = []
        self.max_turns = max_turns

    def add(self, role, content):
        self.turns.append({"role": role, "content": content, "ts": time.time()})
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]

    def get_recent(self, n=5):
        return self.turns[-n:]

    def clear(self):
        self.turns = []


# --- Long-term SQLite memory ---

def _get_conn():
    conn = sqlite3.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            fact TEXT,
            score INTEGER,
            ts REAL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT,
            summary TEXT,
            score INTEGER,
            ts REAL
        )
    """)
    conn.commit()
    return conn


def save_run(task, summary, score):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO runs (task, summary, score, ts) VALUES (?, ?, ?, ?)",
        (task, summary, score, time.time())
    )
    conn.commit()
    conn.close()


def get_past_runs(limit=3):
    conn = _get_conn()
    rows = conn.execute(
        "SELECT task, summary, score FROM runs ORDER BY ts DESC LIMIT ?",
        (limit,)
    ).fetchall()
    conn.close()
    return [{"task": r[0], "summary": r[1], "score": r[2]} for r in rows]


def save_fact(task, fact, score=0):
    conn = _get_conn()
    conn.execute(
        "INSERT INTO facts (task, fact, score, ts) VALUES (?, ?, ?, ?)",
        (task, fact, score, time.time())
    )
    conn.commit()
    conn.close()


def get_all_facts(limit=10):
    conn = _get_conn()
    rows = conn.execute(
        "SELECT fact FROM facts ORDER BY ts DESC LIMIT ?", (limit,)
    ).fetchall()
    conn.close()
    return [r[0] for r in rows]
