import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
DATA_DIR = BASE_DIR / "data"
LOGS_DIR = BASE_DIR / "logs"
OUTPUT_DIR = BASE_DIR / "output_files"
MEMORY_DIR = BASE_DIR / "memory"
DB_PATH = BASE_DIR / "memory" / "long_term.db"

LOGS_DIR.mkdir(exist_ok=True)
OUTPUT_DIR.mkdir(exist_ok=True)
MEMORY_DIR.mkdir(exist_ok=True)

GROQ_MODEL = "llama-3.2-1b-preview"
GROQ_MODEL_MAIN = "llama-3.1-8b-instant"
