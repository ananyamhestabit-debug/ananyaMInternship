import sqlite3
import os

# DB path — always relative to THIS file (memory/long_term.db)
# Works no matter from where you run main.py
DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "long_term.db")


class LongTermMemory:
    def __init__(self):
        self._init_db()

    def _init_db(self):
        # Directory already exists (it's the memory/ folder itself), but just in case:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("""
        CREATE TABLE IF NOT EXISTS memory (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            content TEXT,
            category TEXT
        )
        """)

        # Table for personal facts (key-value)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS facts (
            key TEXT PRIMARY KEY,
            value TEXT
        )
        """)

        conn.commit()
        conn.close()

    def store(self, text, category="general"):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "INSERT INTO memory (content, category) VALUES (?, ?)",
            (text, category)
        )

        conn.commit()
        conn.close()

    def retrieve_all(self):
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT content FROM memory")
        rows = cur.fetchall()

        conn.close()

        return [r[0] for r in rows]

    def save_fact(self, key: str, value: str):
        """Save a personal fact like name, age, job, location."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute(
            "INSERT OR REPLACE INTO facts (key, value) VALUES (?, ?)",
            (key.lower().strip(), value.strip())
        )

        conn.commit()
        conn.close()

    def get_all_facts(self) -> dict:
        """Return all stored personal facts as a dictionary."""
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()

        cur.execute("SELECT key, value FROM facts")
        rows = cur.fetchall()

        conn.close()

        return {row[0]: row[1] for row in rows}