"""
DAY 3 — File Agent
Tool: Read/Write .txt and .csv files
"""

import csv
import os
import json
from groq import Groq

client = Groq()

FILE_AGENT_PROMPT = """You are the File Agent in a multi-agent AI system.

Your ONLY job: Read and analyze file contents provided to you.

When given file content:
- Summarize what the file contains (structure, columns, row count)
- List key statistics if it's a CSV (min, max, totals for numeric columns)
- Identify data quality issues if any (missing values, duplicates)
- Extract raw facts ONLY — no business analysis

Format your response as:
📁 FILE ANALYSIS:
- File type: ...
- Structure: ...
- Key stats: ...
- Raw findings: ...
"""


def read_file(filepath: str) -> str:
    """Reads a .txt or .csv file and returns content as string"""
    if not os.path.exists(filepath):
        return f"ERROR: File not found: {filepath}"

    ext = os.path.splitext(filepath)[1].lower()

    if ext == ".csv":
        rows = []
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                rows.append(row)

        if not rows:
            return "ERROR: CSV file is empty"

        headers = list(rows[0].keys())
        content = f"CSV File: {filepath}\n"
        content += f"Columns: {headers}\n"
        content += f"Total rows: {len(rows)}\n\n"
        content += "--- DATA (first 10 rows) ---\n"

        for i, row in enumerate(rows[:10]):
            content += str(row) + "\n"

        if len(rows) > 10:
            content += f"... and {len(rows) - 10} more rows\n"

        # Compute basic numeric stats
        content += "\n--- FULL DATA ---\n"
        for row in rows:
            content += str(row) + "\n"

        return content

    elif ext == ".txt":
        with open(filepath, "r") as f:
            return f.read()

    else:
        return f"ERROR: Unsupported file type: {ext}"


def write_file(filepath: str, content: str) -> str:
    """Writes content to a .txt file"""
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else ".", exist_ok=True)
    with open(filepath, "w") as f:
        f.write(content)
    return f"✅ File written: {filepath}"


def run_file_agent(instruction: str, filepath: str = None) -> dict:
    """
    Runs the File Agent on a given instruction + optional filepath.
    Returns dict with output and raw file content.
    """
    print(f"\n[FILE AGENT] Instruction: {instruction}")

    raw_content = ""
    if filepath:
        print(f"[FILE AGENT] Reading file: {filepath}")
        raw_content = read_file(filepath)
        print(f"[FILE AGENT] File read complete ({len(raw_content)} chars)")

    user_message = instruction
    if raw_content:
        user_message += f"\n\nFile content:\n{raw_content}"

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": FILE_AGENT_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.3,
        max_tokens=800
    )

    result = response.choices[0].message.content.strip()
    print("[FILE AGENT] Analysis complete ✓")

    return {
        "agent": "file_agent",
        "instruction": instruction,
        "filepath": filepath,
        "raw_content": raw_content,
        "output": result
    }


if __name__ == "__main__":
    # Quick test
    result = run_file_agent(
        instruction="Analyze this CSV file and tell me its structure and key stats",
        filepath="data/sales.csv"
    )
    print(result["output"])
