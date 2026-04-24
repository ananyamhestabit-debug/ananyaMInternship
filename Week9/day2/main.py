"""
DAY 2 — Main Runner
Full 4-Agent Pipeline:
User Query → Orchestrator → Workers (Parallel) → Reflection → Validator → Final Answer
"""

import json
import os
import time
from datetime import datetime

import sys
sys.path.insert(0, os.path.dirname(__file__))

from orchestrator.planner import create_plan
from agents.worker_agent import run_workers_parallel
from agents.reflection_agent import reflect_and_improve
from agents.validator import validate_response


def print_separator(title: str = ""):
    width = 65
    if title:
        pad = (width - len(title) - 2) // 2
        print("\n" + "═" * pad + f" {title} " + "═" * pad)
    else:
        print("\n" + "═" * width)


def print_execution_tree(plan: dict, worker_results: list, validation: dict):
    """Prints simple one-line execution flow"""
    workers = " --> ".join([f"{r['role'].upper()}({r['task_id']})" for r in worker_results])
    print(f"\nFLOW: USER --> ORCHESTRATOR --> {workers} --> REFLECTION --> VALIDATOR --> DONE\n")


def save_log(plan: dict, worker_results: list, reflection: str, validation: dict, elapsed: float):
    # Saves full pipeline run to logs/
    os.makedirs("logs", exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = f"logs/run_{timestamp}.json"

    log_data = {
        "timestamp": timestamp,
        "elapsed_seconds": round(elapsed, 2),
        "plan": plan,
        "worker_results": worker_results,
        "reflection": reflection,
        "validation": validation
    }

    with open(log_file, "w") as f:
        json.dump(log_data, f, indent=2)

    print(f"[LOG] Saved to {log_file}")


def run_pipeline(user_query: str):
    """Full 4-agent pipeline execution"""
    start_time = time.time()

    print_separator("MULTI-AGENT SYSTEM — DAY 2")
    print(f"Query: {user_query}")
    print(f"Time : {datetime.now().strftime('%H:%M:%S')}")

    # ── STEP 1: ORCHESTRATOR creates plan ──
    print_separator("STEP 1: ORCHESTRATOR")
    plan = create_plan(user_query)

    # ── STEP 2: WORKERS run in parallel ──
    print_separator("STEP 2: PARALLEL WORKERS")
    worker_results = run_workers_parallel(plan["tasks"])

    for r in worker_results:
        print(f"\n--- {r['role'].upper()} OUTPUT (Task {r['task_id']}) ---")
        print(r["output"])

    # ── STEP 3: REFLECTION AGENT synthesizes ──
    print_separator("STEP 3: REFLECTION AGENT")
    reflection = reflect_and_improve(user_query, worker_results)
    print("\n" + reflection)

    # ── STEP 4: VALIDATOR checks quality ──
    print_separator("STEP 4: VALIDATOR")
    validation = validate_response(user_query, reflection)

    # ── FINAL OUTPUT ──
    print_separator("FINAL ANSWER")
    final = validation.get("final_answer", reflection)
    if isinstance(final, dict):
        for k, v in final.items():
            print(f"\n**{k}**\n{v}")
    else:
        print(final)

    elapsed = time.time() - start_time

    # ── EXECUTION FLOW ──
    print_separator("EXECUTION FLOW")
    print_execution_tree(plan, worker_results, validation)
    print(f"Status : {validation.get('validation_status', 'PASS')} | Score: {validation.get('score', 'N/A')}/10")
    print(f"Time   : {elapsed:.2f}s")

    # ── SAVE LOG ──
    save_log(plan, worker_results, reflection, validation, elapsed)

    return validation.get("final_answer", reflection)


EXAMPLE_QUERIES = [
    "Explain the differences between SQL and NoSQL databases and when to use each",
    "How do I build a REST API in Python using FastAPI?",
    "What is machine learning and what are its main types?",
]

if __name__ == "__main__":
    print("\nAvailable example queries:")
    for i, q in enumerate(EXAMPLE_QUERIES, 1):
        print(f"  {i}. {q}")

    print("\nEnter your query (or press Enter to use example 1): ", end="")
    user_input = input().strip()

    if not user_input:
        query = EXAMPLE_QUERIES[0]
    elif user_input.isdigit() and 1 <= int(user_input) <= len(EXAMPLE_QUERIES):
        query = EXAMPLE_QUERIES[int(user_input) - 1]
    else:
        query = user_input

    run_pipeline(query)
