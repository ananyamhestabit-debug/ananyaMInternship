import json
import os

os.makedirs("logs", exist_ok=True)

LOG_FILE = "logs/CHAT-LOGS.json"

def log(data):
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True) if "/" in LOG_FILE else None

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(data) + "\n")