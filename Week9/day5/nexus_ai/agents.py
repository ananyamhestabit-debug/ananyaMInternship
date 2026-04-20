"""
agents.py
All 9 NEXUS AI agents. Each function = one agent.
Called in sequence by main.py.
"""

import json, re, os, csv
from nexus_ai.llm_client import call_llm
from nexus_ai.config import DATA_DIR


def _read_csv_summary(csv_path: str = "") -> str:
    """
    Reads the given CSV file and returns a plain-text summary to inject into prompts.
    Returns empty string if path not given or file not found.
    """
    if not csv_path or not os.path.exists(csv_path):
        return ""

    rows = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        headers = reader.fieldnames or []
        for row in reader:
            rows.append(row)

    if not rows:
        return ""

    total_rows = len(rows)

    # find sales/revenue column and sum it
    sales_col = next((h for h in headers if "sales" in h.lower() or "revenue" in h.lower()), None)
    total_sales = 0.0
    if sales_col:
        for r in rows:
            try:
                total_sales += float(r[sales_col])
            except (ValueError, KeyError):
                pass

    # top 5 sample rows
    sample_text = "\n".join([str(r) for r in rows[:5]])

    # categorical column unique values
    cat_lines = []
    for h in headers:
        vals = list(set(r[h] for r in rows if r.get(h)))
        if 2 <= len(vals) <= 15:
            cat_lines.append(f"  {h}: {', '.join(sorted(vals)[:10])}")

    summary = (
        f"REAL CSV DATA FROM {os.path.basename(csv_path)}:\n"
        f"  Columns   : {', '.join(headers)}\n"
        f"  Total rows: {total_rows}\n"
        f"  Total {sales_col or 'sales'}: {round(total_sales, 2)}\n\n"
        f"Sample rows (first 5):\n{sample_text}\n\n"
        f"Unique values in categorical columns:\n" + "\n".join(cat_lines)
    )
    return summary


# ── 1. ORCHESTRATOR ───────────────────────────────────────────────────────────

def orchestrator(task: str) -> dict:
    print("[ORCHESTRATOR] Breaking task into high-level steps...")
    system = """You are an AI orchestrator. Given a task, return ONLY this JSON:
{
  "task": "<original task>",
  "goal": "<one sentence goal>",
  "steps": ["step1", "step2", "step3", "step4", "step5"]
}
No markdown. No explanation. Just the JSON."""
    raw = call_llm(system, f"Task: {task}", max_tokens=400)
    m = re.search(r'\{.*\}', raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return {
        "task": task,
        "goal": f"Complete: {task}",
        "steps": ["Gather requirements", "Research", "Analyse", "Generate output", "Review"],
    }


# ── 2. PLANNER ────────────────────────────────────────────────────────────────

def planner(orch: dict) -> dict:
    print("[PLANNER] Expanding steps into detailed sub-tasks...")
    system = """You are a project planner. Return ONLY this JSON:
{
  "plan": [
    {"step": 1, "task": "<detailed task>", "owner": "<researcher|coder|analyst>", "output": "<expected output>"}
  ]
}"""
    raw = call_llm(system, f"Goal: {orch['goal']}\nSteps: {json.dumps(orch['steps'])}", max_tokens=600)
    m = re.search(r'\{.*\}', raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return {
        "plan": [
            {"step": i+1, "task": s, "owner": "researcher", "output": "findings"}
            for i, s in enumerate(orch["steps"])
        ]
    }


# ── 3. RESEARCHER ─────────────────────────────────────────────────────────────

def researcher(task: str, plan: dict, csv_path: str = "") -> str:
    print("[RESEARCHER] Gathering relevant information...")

    csv_data = _read_csv_summary(csv_path)
    if csv_data:
        print("[RESEARCHER] Real CSV data found — injecting into analysis...")

    system = "You are a research agent. Analyse the provided data thoroughly. Use clear section headers and be specific with numbers from the data."

    prompt = f"Task: {task}\nPlan:\n{json.dumps(plan, indent=2)}"
    if csv_data:
        prompt += f"\n\n{csv_data}\n\nBase your analysis on the REAL DATA above. Quote actual numbers, column names, and values."

    return call_llm(system, prompt, max_tokens=900, temperature=0.3)


# ── 4. CODER ──────────────────────────────────────────────────────────────────

def coder(task: str, research: str, csv_path: str = "") -> str:
    print("[CODER] Writing code and technical implementation...")

    csv_data = _read_csv_summary(csv_path)

    system = """You are a software engineer agent.
Write clean, well-commented Python code.
Always wrap code in ```python ... ``` blocks.
If the task is not code-related, write a technical implementation plan instead."""

    prompt = f"Task: {task}\n\nContext from research:\n{research[:600]}"
    if csv_data:
        prompt += f"\n\nCSV file info:\n{csv_data[:400]}\n\nUse 'data/sales.csv' as the file path in the code."

    return call_llm(system, prompt, max_tokens=1000, temperature=0.2)


# ── 5. ANALYST ────────────────────────────────────────────────────────────────

def analyst(task: str, research: str, code_out: str, csv_path: str = "") -> str:
    print("[ANALYST] Synthesizing findings into structured insights...")

    csv_data = _read_csv_summary(csv_path)

    system = "You are a business and data analyst. Synthesize findings into structured insights. Use numbered lists and clear headers. Be specific with real numbers where available."

    prompt = (
        f"Task: {task}\n\n"
        f"Research:\n{research[:500]}\n\n"
        f"Technical output:\n{code_out[:400]}\n\n"
    )
    if csv_data:
        prompt += f"Real data context:\n{csv_data[:400]}\n\n"
    prompt += "Provide:\n1. Key findings (with real numbers)\n2. Recommendations\n3. Risks or limitations"

    return call_llm(system, prompt, max_tokens=700, temperature=0.3)


# ── 6. CRITIC ─────────────────────────────────────────────────────────────────

def critic(task: str, analysis: str) -> dict:
    print("[CRITIC] Reviewing output for weaknesses...")
    system = """You are a critical review agent. Find flaws and gaps. Return ONLY this JSON:
{
  "score": <1-10>,
  "strengths": ["s1", "s2"],
  "weaknesses": ["w1", "w2"],
  "missing": ["m1"]
}"""
    raw = call_llm(system, f"Task: {task}\n\nAnalysis:\n{analysis[:700]}", max_tokens=400)
    m = re.search(r'\{.*\}', raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return {"score": 7, "strengths": ["Comprehensive"], "weaknesses": ["Could be more specific"], "missing": []}


# ── 7. OPTIMIZER ──────────────────────────────────────────────────────────────

def optimizer(task: str, analysis: str, critique: dict) -> str:
    print("[OPTIMIZER] Improving output based on critic feedback...")
    system = "You are an optimisation agent. Improve the analysis by addressing every weakness and gap the critic found."
    prompt = (
        f"Task: {task}\n\n"
        f"Original analysis:\n{analysis[:600]}\n\n"
        f"Weaknesses: {critique.get('weaknesses', [])}\n"
        f"Missing:    {critique.get('missing', [])}\n\n"
        "Write an improved version."
    )
    return call_llm(system, prompt, max_tokens=800, temperature=0.3)


# ── 8. VALIDATOR ──────────────────────────────────────────────────────────────

def validator(task: str, optimized: str) -> dict:
    print("[VALIDATOR] Running final quality checks...")
    system = """You are a quality validation agent. Return ONLY this JSON:
{
  "passed": true,
  "score": <1-10>,
  "verdict": "<one sentence>",
  "issues": []
}"""
    raw = call_llm(system, f"Task: {task}\n\nOutput:\n{optimized[:700]}", max_tokens=300)
    m = re.search(r'\{.*\}', raw, re.DOTALL)
    if m:
        try:
            return json.loads(m.group())
        except Exception:
            pass
    return {"passed": True, "score": 8, "verdict": "Output meets requirements.", "issues": []}


# ── 9. REPORTER ───────────────────────────────────────────────────────────────

def reporter(task: str, all_outputs: dict) -> str:
    print("[REPORTER] Compiling final report...")
    system = """You are a reporting agent.
Compile all agent work into one clean professional report.
Sections: Executive Summary, Key Findings, Implementation, Recommendations, Conclusion."""
    prompt = (
        f"Task: {task}\n\n"
        f"Research:  {str(all_outputs.get('research',''))[:400]}\n"
        f"Analysis:  {str(all_outputs.get('analysis',''))[:400]}\n"
        f"Optimized: {str(all_outputs.get('optimized',''))[:400]}\n"
        f"Validation: passed={all_outputs.get('validation',{}).get('passed')} "
        f"score={all_outputs.get('validation',{}).get('score')}\n\n"
        "Write the final report."
    )
    return call_llm(system, prompt, max_tokens=1000, temperature=0.4)
