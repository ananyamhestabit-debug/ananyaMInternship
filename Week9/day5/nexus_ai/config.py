import os

GROQ_MODEL  = "llama-3.1-8b-instant"
AGENT_SLEEP = 2  # seconds between API calls to avoid rate limit

BASE_DIR    = os.path.dirname(os.path.dirname(__file__))
LOG_DIR     = os.path.join(BASE_DIR, "logs")
MEMORY_DIR  = os.path.join(BASE_DIR, "memory")
OUTPUT_DIR  = os.path.join(BASE_DIR, "output_files")
DATA_DIR = os.path.join(BASE_DIR, 'data')