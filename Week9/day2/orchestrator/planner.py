"""
DAY 2 — Orchestrator / Planner Agent
Breaks user query into sub-tasks and delegates to Worker Agents
"""

import json
import re
from groq import Groq

client = Groq()  # reads GROQ_API_KEY from env

PLANNER_SYSTEM_PROMPT = """You are the Orchestrator/Planner agent in a multi-agent AI system.

Your ONLY job:
1. Receive a user query
2. Break it into 2-4 clear, atomic sub-tasks
3. Assign each sub-task to one of these worker roles: [researcher, analyst, coder]
4. Return a structured JSON execution plan

STRICT OUTPUT FORMAT — return ONLY this JSON, no extra text:
{
  "original_query": "<user query>",
  "plan_id": "<short unique id like PLAN-001>",
  "tasks": [
    {
      "task_id": "T1",
      "assigned_to": "researcher",
      "instruction": "<specific instruction for this worker>"
    },
    {
      "task_id": "T2",
      "assigned_to": "analyst",
      "instruction": "<specific instruction for this worker>"
    }
  ]
}

Rules:
- Keep each instruction focused and specific
- Do NOT execute tasks yourself
- Do NOT include any explanation outside the JSON
- Always assign at least 2 tasks
"""

def create_plan(user_query: str) -> dict:
    """Takes user query, returns structured execution plan as dict"""
    print(f"\n[ORCHESTRATOR] Received query: {user_query}")
    print("[ORCHESTRATOR] Creating execution plan...")

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": PLANNER_SYSTEM_PROMPT},
            {"role": "user", "content": f"Create a plan for: {user_query}"}
        ],
        temperature=0.3,
        max_tokens=600
    )

    raw = response.choices[0].message.content.strip()

    # Extract JSON even if model adds small prefix/suffix
    json_match = re.search(r'\{.*\}', raw, re.DOTALL)
    if json_match:
        plan = json.loads(json_match.group())
    else:
        raise ValueError(f"Planner did not return valid JSON.\nRaw output:\n{raw}")

    print(f"[ORCHESTRATOR] Plan created with {len(plan['tasks'])} tasks")
    for t in plan["tasks"]:
        print(f"  → {t['task_id']} | Assigned to: {t['assigned_to']} | {t['instruction'][:60]}...")

    return plan
