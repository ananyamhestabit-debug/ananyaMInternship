"""
DAY 3 — Orchestrator
Decides which tool agents (file/code/db) to invoke and in what order
"""

import json
import re
import time
from groq import Groq

client = Groq()

ORCHESTRATOR_PROMPT = """You are the Orchestrator in a tool-using multi-agent AI system.

Available tool agents:
- "file_agent"  → reads/writes .txt and .csv files
- "code_agent"  → writes and executes Python code for analysis/computation
- "db_agent"    → runs SQL queries on SQLite database (table: sales)

Given a user query, create an ordered execution plan.

Return ONLY this JSON:
{
  "query": "<original query>",
  "plan": [
    {
      "step": 1,
      "agent": "file_agent",
      "instruction": "<specific instruction>",
      "filepath": "<path if needed, else null>"
    },
    {
      "step": 2,
      "agent": "code_agent",
      "instruction": "<specific instruction>"
    }
  ]
}

Rules:
- For CSV analysis tasks: use file_agent first, then code_agent, then db_agent
- For pure SQL tasks: use only db_agent
- For computation tasks: use code_agent
- Keep instructions specific and actionable
- filepath only for file_agent steps that need to read a file
- ALWAYS use "data/sales.csv" as the filepath (never just "sales.csv")
"""


def create_tool_plan(user_query: str) -> dict:
    """Creates an ordered execution plan for tool agents"""
    print(f"\n[ORCHESTRATOR] Query: {user_query}")
    print("[ORCHESTRATOR] Creating tool execution plan...")

    time.sleep(1)

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": ORCHESTRATOR_PROMPT},
            {"role": "user", "content": f"Create a plan for: {user_query}"}
        ],
        temperature=0.2,
        max_tokens=600
    )

    raw = response.choices[0].message.content.strip()

    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        clean = json_match.group().replace('\n', ' ').replace('\r', ' ')
        plan = json.loads(clean)
    else:
        plan = {
            "query": user_query,
            "plan": [
                {"step": 1, "agent": "file_agent", "instruction": f"Read and analyze the CSV file for: {user_query}", "filepath": "data/sales.csv"},
                {"step": 2, "agent": "db_agent", "instruction": f"Query the database to answer: {user_query}"},
                {"step": 3, "agent": "code_agent", "instruction": f"Write Python code to compute insights for: {user_query}"}
            ]
        }

    # Fix filepath if model forgot to add data/ prefix
    for step in plan["plan"]:
        if step.get("filepath") and not step["filepath"].startswith("data/"):
            step["filepath"] = "data/" + step["filepath"].replace("data/", "")

    print(f"[ORCHESTRATOR] Plan created with {len(plan['plan'])} steps:")
    for step in plan["plan"]:
        fp = f" | file: {step.get('filepath')}" if step.get("filepath") else ""
        print(f"  Step {step['step']}: {step['agent']}{fp}")

    return plan
