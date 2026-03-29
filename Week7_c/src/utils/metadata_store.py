import json
import os

def save_metadata(metadata, path="src/data/chunks/metadata.json"):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w") as f:
        json.dump(metadata, f, indent=4)