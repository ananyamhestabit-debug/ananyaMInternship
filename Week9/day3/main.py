"""
DAY 3 — Main Runner
Tool-Calling Multi-Agent System
User Query → Orchestrator → Tool Agents (File/Code/DB) → Analysis → Final Answer
"""

import json
import os
import sys
import time
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from orchestrator.tool_orchestrator import create_tool_plan
from tools.file_agent import run_file_agent
from tools.code_executor import run_code_agent
from tools.db_agent import run_db_agent, init_db_from_csv
from agents.analysis_agent import run_analysis_agent


def print_separator(title: str = ""):
    width = 65
    if title:
        pad = (width - len(title) - 2) // 2
        print("\n" + "═" * pad + f" {title} " + "═" * pad)
    else:
        print("\n" + "═" * width)


def dispatch_tool_agent(step: dict, context: str = "") -> dict:
    """Routes a step to the correct tool agent"""
    agent = step["agent"]
    instruction = step["instruction"]
    filepath = step.get("filepath")

    if agent == "file_agent":
        return run_file_agent(instruction, filepath)
    elif agent == "code_agent":
        return run_code_agent(instruction, context)
    elif agent == "db_agent":
        return run_db_agent(instruction)
    else:
        return {"agent": agent, "instruction": instruction, "output": f"Unknown agent: {agent}"}


def print_tool_chain(plan: dict, tool_outputs: list):
    agents = " --> ".join([s["agent"].replace("_", " ").upper() for s in plan["plan"]])
    print(f"\nFLOW: USER --> ORCHESTRATOR --> {agents} --> ANALYSIS --> DONE\n")


def save_log(plan: dict, tool_outputs: list, final_answer: str, elapsed: float):
    """Saves run to logs/"""
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/run_{timestamp}.json"

    safe_outputs = []
    for o in tool_outputs:
        safe = {k: v for k, v in o.items() if k not in ["raw_content", "execution"]}
        safe_outputs.append(safe)

    log_data = {
        "timestamp": timestamp,
        "elapsed_seconds": round(elapsed, 2),
        "plan": plan,
        "tool_outputs": safe_outputs,
        "final_answer": final_answer
    }

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)

    print(f"[LOG] Saved to {log_file}")


def run_pipeline(user_query: str):
    """Full Day 3 pipeline: Orchestrator → Tools → Analysis"""
    start_time = time.time()

    print_separator("TOOL-CALLING MULTI-AGENT SYSTEM — DAY 3")
    print(f"Query : {user_query}")
    print(f"Time  : {datetime.now().strftime('%H:%M:%S')}")

    # ── INIT DB ──
    print("\n[SETUP] Initializing SQLite database from CSV...")
    init_db_from_csv()

    # ── STEP 1: ORCHESTRATOR ──
    print_separator("STEP 1: ORCHESTRATOR")
    plan = create_tool_plan(user_query)

    # ── STEP 2: TOOL AGENTS ──
    print_separator("STEP 2: TOOL AGENTS")
    tool_outputs = []
    accumulated_context = ""

    for step in plan["plan"]:
        print(f"\n>>> Running Step {step['step']}: {step['agent'].upper()}")
        result = dispatch_tool_agent(step, context=accumulated_context)
        tool_outputs.append(result)

        print(f"\n--- {result['agent'].upper()} OUTPUT ---")
        print(result["output"][:1500])
        if len(result["output"]) > 1500:
            print("... [truncated for display]")

        accumulated_context += f"\n{result['agent']} output:\n{result['output'][:500]}\n"
        time.sleep(1)

    # ── STEP 3: ANALYSIS AGENT ──
    print_separator("STEP 3: ANALYSIS AGENT")
    final_answer = run_analysis_agent(user_query, tool_outputs)

    # ── FINAL OUTPUT ──
    print_separator("FINAL REPORT")
    print(final_answer)

    elapsed = time.time() - start_time

    # ── FLOW ──
    print_separator("EXECUTION FLOW")
    print_tool_chain(plan, tool_outputs)
    print(f"Time : {elapsed:.2f}s")

    # ── SAVE LOG ──
    save_log(plan, tool_outputs, final_answer, elapsed)

    return final_answer


EXAMPLE_QUERIES = [
    "Analyze sales.csv and generate top 5 business insights",
    "Which product has the highest total revenue? Show SQL query",
    "Calculate month-wise revenue trend using Python code",
]

if __name__ == "__main__":
    print("\nAvailable example queries:")
    for i, q in enumerate(EXAMPLE_QUERIES, 1):
        print(f"  {i}. {q}")

    print("\nEnter your query (or press Enter for example 1): ", end="")
    user_input = input().strip()

    if not user_input:
        query = EXAMPLE_QUERIES[0]
    elif user_input.isdigit() and 1 <= int(user_input) <= len(EXAMPLE_QUERIES):
        query = EXAMPLE_QUERIES[int(user_input) - 1]
    else:
        query = user_input

    run_pipeline(query)
