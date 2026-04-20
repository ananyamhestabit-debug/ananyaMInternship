"""
DAY 5 - NEXUS AI
Autonomous 9-agent system.

Output saving rules:
  - Code query (build/write/implement/api/pipeline etc.)
        -> output_files/output_TIMESTAMP.py        (code)
        -> output_files/output_TIMESTAMP_report.md (report)
        -> CLI also prints full output
  - Any other query
        -> CLI prints full output ONLY, no file saved
"""

import json, os, sys, time
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from nexus_ai.config import LOG_DIR, OUTPUT_DIR
from nexus_ai.memory import save_run, get_past_runs
from nexus_ai.output_saver import _is_code_task, save_py, save_md
from nexus_ai import agents

os.makedirs(LOG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

EXAMPLES = [
    "Plan a startup in AI for healthcare",
    "Write a Python FastAPI REST API with CRUD endpoints for a todo app",
    "Analyze a CSV sales dataset and create a business strategy",
    "Build a machine learning pipeline for text classification in Python",
    "Design a RAG pipeline for 50000 documents",
    "Generate backend architecture for a scalable e-commerce app",
]


def line(label: str = ""):
    print(f"\n{'─' * 60}")
    if label:
        print(f"  {label}")
        print(f"{'─' * 60}")


def run_nexus(task: str, csv_path: str = ""):
    t0 = time.time()
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")

    line("NEXUS AI  —  Autonomous Multi-Agent System")
    print(f"  Task : {task}")
    print(f"  Time : {datetime.now().strftime('%H:%M:%S')}")

    if csv_path:
        print(f"  CSV  : {csv_path}")

    # show memory from past runs
    past = get_past_runs(limit=2)
    if past:
        print(f"\n  [MEMORY] {len(past)} past run(s) recalled:")
        for p in past:
            print(f"    task : {p['task'][:50]}")
            print(f"    score: {p['score']}  saved: {p['saved_file']}  date: {p['timestamp'][:10]}")

    out = {}

    # ── 1. ORCHESTRATOR
    line("1 / 9   ORCHESTRATOR")
    orch = agents.orchestrator(task)
    out["orchestrator"] = orch
    print(f"  Goal : {orch.get('goal','')}")
    for i, s in enumerate(orch.get("steps", []), 1):
        print(f"    {i}. {s}")

    # ── 2. PLANNER
    line("2 / 9   PLANNER")
    plan = agents.planner(orch)
    out["planner"] = plan
    for item in plan.get("plan", []):
        print(f"  [{item['step']}] {item['task'][:55]}  ->  owner: {item['owner']}")

    # ── 3. RESEARCHER
    line("3 / 9   RESEARCHER")
    research = agents.researcher(task, plan, csv_path)
    out["research"] = research
    print(research)

    # ── 4. CODER
    line("4 / 9   CODER")
    code_out = agents.coder(task, research, csv_path)
    out["code"] = code_out
    print(code_out)

    # ── 5. ANALYST
    line("5 / 9   ANALYST")
    analysis = agents.analyst(task, research, code_out, csv_path)
    out["analysis"] = analysis
    print(analysis)

    # ── 6. CRITIC
    line("6 / 9   CRITIC")
    critique = agents.critic(task, analysis)
    out["critic"] = critique
    print(f"  Score     : {critique.get('score')}/10")
    print(f"  Strengths : {critique.get('strengths', [])}")
    print(f"  Weaknesses: {critique.get('weaknesses', [])}")
    print(f"  Missing   : {critique.get('missing', [])}")

    # ── 7. OPTIMIZER
    line("7 / 9   OPTIMIZER")
    optimized = agents.optimizer(task, analysis, critique)
    out["optimized"] = optimized
    print(optimized)

    # ── 8. VALIDATOR
    line("8 / 9   VALIDATOR")
    validation = agents.validator(task, optimized)
    out["validation"] = validation
    status = "PASS" if validation.get("passed") else "FAIL"
    print(f"  Status : {status}")
    print(f"  Score  : {validation.get('score')}/10")
    print(f"  Verdict: {validation.get('verdict')}")

    # ── 9. REPORTER
    line("9 / 9   REPORTER")
    final_report = agents.reporter(task, out)
    out["final_report"] = final_report

    # ── FINAL OUTPUT IN CLI
    elapsed = round(time.time() - t0, 2)
    line("FINAL REPORT")
    print(final_report)

    agent_flow = (
        "USER -> ORCHESTRATOR -> PLANNER -> RESEARCHER -> CODER -> "
        "ANALYST -> CRITIC -> OPTIMIZER -> VALIDATOR -> REPORTER -> DONE"
    )
    print(f"\nFLOW  : {agent_flow}")
    print(f"Status: {status} | Score: {validation.get('score')}/10 | Time: {elapsed}s")

    # ── SAVE OUTPUT FILE (only for code queries, based on task text only)
    is_code = _is_code_task(task)   # checks task string only, not generated content
    saved_file = "none"

    if is_code:
        # Code query -> .py (code) + .md (report)
        line("OUTPUT FILES")
        py_path = save_py(task, code_out, ts)
        md_path = save_md(task, final_report, ts, suffix="_report")
        print(f"  Query type   : CODE")
        print(f"  Code saved   : {py_path}")
        print(f"  Report saved : {md_path}")
        saved_file = os.path.basename(py_path)
    else:
        # Non-code query -> CLI only, no file
        print(f"\n  [No file saved — output printed in terminal above]")

    # ── SAVE JSON LOG
    log_path = os.path.join(LOG_DIR, f"nexus_run_{ts}.json")
    with open(log_path, "w") as f:
        json.dump({
            "task": task,
            "timestamp": ts,
            "elapsed_seconds": elapsed,
            "validation_score": validation.get("score"),
            "saved_file": saved_file,
            "outputs": {k: str(v)[:500] for k, v in out.items()},
        }, f, indent=2)
    print(f"  Log saved    : {log_path}")

    # ── SAVE TO LONG-TERM MEMORY
    save_run(task, validation.get("score", 0), saved_file)


def main():
    print("=" * 60)
    print("  NEXUS AI  —  Day 5  —  Week 9 Assessment")
    print("=" * 60)
    print("\nExample tasks:")
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"  {i}. {ex}")
    print()

    user_input = input("Enter task number (1-6) or type your own task: ").strip()

    if user_input.isdigit() and 1 <= int(user_input) <= len(EXAMPLES):
        task = EXAMPLES[int(user_input) - 1]
    elif user_input == "":
        task = EXAMPLES[0]
    else:
        task = user_input

    # ask for CSV path if task mentions csv/data/analyze/dataset
    csv_path = ""
    csv_keywords = ["csv", "dataset", "data file", "analyze", "analyse", "sales data"]
    if any(kw in task.lower() for kw in csv_keywords):
        print()
        csv_input = input("CSV file path (press Enter to skip): ").strip()
        if csv_input:
            if os.path.exists(csv_input):
                csv_path = csv_input
                print(f"  CSV loaded: {csv_input}")
            else:
                print(f"  File not found: {csv_input} — continuing without CSV")

    print(f"\nStarting NEXUS AI on: {task}")
    print("9 agents will run sequentially — takes ~3-4 minutes (rate limit buffer).\n")
    run_nexus(task, csv_path)


if __name__ == "__main__":
    main()
