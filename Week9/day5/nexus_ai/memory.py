import os, sqlite3
from datetime import datetime
from nexus_ai.config import MEMORY_DIR

os.makedirs(MEMORY_DIR, exist_ok=True)
DB = os.path.join(MEMORY_DIR, "nexus_memory.db")

def _init():
    c = sqlite3.connect(DB)
    c.execute("""CREATE TABLE IF NOT EXISTS runs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT, score INTEGER, saved_file TEXT, timestamp TEXT
    )""")
    c.commit(); c.close()

def save_run(task: str, score: int, saved_file: str):
    _init()
    c = sqlite3.connect(DB)
    c.execute("INSERT INTO runs (task,score,saved_file,timestamp) VALUES (?,?,?,?)",
              (task, score, saved_file, datetime.now().isoformat()))
    c.commit(); c.close()

def get_past_runs(limit: int = 3) -> list:
    _init()
    c = sqlite3.connect(DB)
    rows = c.execute("SELECT task,score,saved_file,timestamp FROM runs ORDER BY id DESC LIMIT ?",
                     (limit,)).fetchall()
    c.close()
    return [{"task": r[0], "score": r[1], "saved_file": r[2], "timestamp": r[3]} for r in rows]
