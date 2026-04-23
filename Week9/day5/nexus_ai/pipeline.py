import json
import time
import os
from datetime import datetime
from nexus_ai import agents
from nexus_ai.memory import (
    SessionMemory, save_run, get_past_runs, save_fact, get_all_facts
)
from nexus_ai.output_saver import save_output
from nexus_ai.config import LOGS_DIR

try:
    from nexus_ai.vector_store import store_vector, search_similar
    VECTOR_ENABLED = True
except Exception:
    VECTOR_ENABLED = False

session = SessionMemory()


def run_pipeline(task, csv_path=None, stream_callback=None):
    """
    Run the full 9-agent NEXUS AI pipeline.
    stream_callback(msg): called with each log line.
    Returns dict with keys: report, validator, py_file, md_file, log_path, flow, score, elapsed
    """

    def log(msg):
        if stream_callback:
            stream_callback(msg)

    start = time.time()
    log(f"[NEXUS AI] Task: {task}")

    # Memory recall
    past_runs = get_past_runs(3)
    memory_context = ""
    if past_runs:
        lines = [f"  task: {r['task']}. score: {r['score']}" for r in past_runs]
        memory_context = "\n".join(lines)
        log(f"[MEMORY] {len(past_runs)} past run(s) recalled")

    # CSV loading
    csv_summary = ""
    sql_insights = ""
    if csv_path:
        from tools.csv_tool import read_csv_summary
        csv_summary = read_csv_summary(csv_path) or ""
        if csv_summary:
            log(f"[CSV] Loaded: {os.path.basename(csv_path)}")

        # NL to SQL pipeline
        try:
            from tools.nl_sql_tool import csv_insights
            log("[SQL] Running NL to SQL analysis on CSV...")
            sql_insights = csv_insights(csv_path, task)
            log("[SQL] Done.")
        except Exception as e:
            log(f"[SQL] Skipped: {e}")

    # --- ORCHESTRATOR ---
    log("[ORCHESTRATOR] Planning pipeline...")
    orch = agents.orchestrator(task, memory_context)
    pipeline = orch.get("pipeline", ["planner", "researcher", "analyst", "critic", "optimizer", "validator", "reporter"])
    flow = "USER --> ORCHESTRATOR --> " + " --> ".join(a.upper() for a in pipeline) + " --> DONE"
    log(f"FLOW: {flow}")

    # --- PLANNER ---
    log("[PLANNER] Creating execution steps...")
    plan = agents.planner(task, orch.get("notes", ""))
    steps = plan.get("steps", [])
    if steps:
        for s in steps:
            log(f"  Step {s.get('step','?')}: [{s.get('agent','?').upper()}] {s.get('action','')}")

    # --- RESEARCHER ---
    research = ""
    if "researcher" in pipeline:
        log("[RESEARCHER] Gathering context...")
        facts = get_all_facts(3)
        research = agents.researcher(task, csv_summary, facts)
        log("[RESEARCHER] Done.")

    # --- CODER ---
    code_output = ""
    if "coder" in pipeline:
        log("[CODER] Writing code...")
        code_output = agents.coder(task, research)
        log("[CODER] Done.")

    combined = research
    if code_output:
        combined += "\n\n" + code_output

    # --- ANALYST ---
    analysis = ""
    if "analyst" in pipeline:
        log("[ANALYST] Analyzing data and generating insights...")
        analysis = agents.analyst(task, research, csv_summary, sql_insights)
        if sql_insights:
            log("[ANALYST] SQL insights included in analysis.")
        combined += "\n\n" + analysis
        log("[ANALYST] Done.")

    # --- CRITIC ---
    log("[CRITIC] Reviewing output quality...")
    critic_result = agents.critic(task, combined)
    critic_score = critic_result.get("score", 7)
    issues = critic_result.get("issues", [])
    log(f"[CRITIC] Score: {critic_score}/10 | Issues: {len(issues)}")
    for issue in issues:
        log(f"  - {issue}")

    # --- OPTIMIZER ---
    log("[OPTIMIZER] Improving output...")
    optimized = agents.optimizer(task, combined, critic_result)
    log("[OPTIMIZER] Done.")

    # --- VALIDATOR ---
    log("[VALIDATOR] Validating final output...")
    validator_result = agents.validator(task, optimized)
    status = validator_result.get("status", "PASS")
    score = validator_result.get("score", 8)
    log(f"[VALIDATOR] {status} | Score: {score}/10 | {validator_result.get('verdict','')}")

    # Self-reflection pass if score is low
    if score < 7:
        log("[SELF-REFLECTION] Score low — running second optimization pass...")
        optimized = agents.optimizer(task, optimized, {
            "issues": ["output quality too low"],
            "suggestions": ["be more detailed, specific, and complete"]
        })
        validator_result = agents.validator(task, optimized)
        score = validator_result.get("score", score)
        log(f"[VALIDATOR] Retry: {validator_result.get('status')} | Score: {score}/10")

    # --- REPORTER ---
    log("[REPORTER] Generating final report...")
    report = agents.reporter(task, validator_result, steps, critic_score, validator_result)
    log("[REPORTER] Done.")

    # Save output files
    raw_final = validator_result.get("final_answer", optimized)
    if isinstance(raw_final, dict):
        raw_final = json.dumps(raw_final, indent=2)
    final_content = str(raw_final)

    py_file, md_file = save_output(task, final_content + "\n\n" + report)
    if py_file:
        log(f"[SAVED] Code: {py_file}")
        log(f"[SAVED] Report: {md_file}")
    else:
        log("[OUTPUT] Non-code task — no file saved, output shown above")

    # Memory save
    save_run(task, report[:300], score)
    save_fact(task, f"Completed: '{task[:80]}' score={score}")
    session.add("user", task)
    session.add("assistant", report[:200])
    if VECTOR_ENABLED:
        try:
            store_vector(f"Task: {task} | Summary: {report[:200]}")
        except Exception:
            pass

    # Log save
    elapsed = round(time.time() - start, 2)
    log_data = {
        "task": task,
        "flow": flow,
        "steps": steps,
        "critic_score": critic_score,
        "validator": validator_result,
        "elapsed_seconds": elapsed,
        "timestamp": datetime.now().isoformat(),
        "py_file": py_file,
        "md_file": md_file,
        "sql_insights_used": bool(sql_insights),
    }
    log_path = LOGS_DIR / f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    log_path.write_text(json.dumps(log_data, indent=2), encoding="utf-8")
    log(f"[LOG] Saved: {log_path}")
    log(f"[DONE] Total time: {elapsed}s")

    return {
        "report": report,
        "validator": validator_result,
        "py_file": py_file,
        "md_file": md_file,
        "log_path": str(log_path),
        "flow": flow,
        "score": score,
        "elapsed": elapsed,
    }