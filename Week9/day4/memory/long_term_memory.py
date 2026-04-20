"""
DAY 4 - Long-term Memory (SQLite)
Stores important facts and summaries that persist across sessions.
"""

import sqlite3
import os
from datetime import datetime

DB_PATH = "memory/long_term.db"


def init_db():
    os.makedirs("memory", exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS memories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            type TEXT,
            content TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_memory(content: str, memory_type: str = "fact"):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute(
        "INSERT INTO memories (timestamp, type, content) VALUES (?, ?, ?)",
        (datetime.now().isoformat(), memory_type, content)
    )
    conn.commit()
    conn.close()


def get_all_memories(memory_type: str = None) -> list:
    init_db()
    conn = sqlite3.connect(DB_PATH)
    if memory_type:
        rows = conn.execute(
            "SELECT id, timestamp, type, content FROM memories WHERE type=? ORDER BY id DESC LIMIT 50",
            (memory_type,)
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT id, timestamp, type, content FROM memories ORDER BY id DESC LIMIT 50"
        ).fetchall()
    conn.close()
    return [{"id": r[0], "timestamp": r[1], "type": r[2], "content": r[3]} for r in rows]


def delete_memory(memory_id: int):
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM memories WHERE id=?", (memory_id,))
    conn.commit()
    conn.close()


def clear_all():
    init_db()
    conn = sqlite3.connect(DB_PATH)
    conn.execute("DELETE FROM memories")
    conn.commit()
    conn.close()
