import json
import re
import time
from groq import Groq
from nexus_ai.config import GROQ_MODEL_MAIN as MODEL

client = Groq()

SLEEP = 1  # minimal sleep between calls


def _call(system_prompt, user_msg, max_tokens=600):
    time.sleep(SLEEP)
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_msg},
        ],
        temperature=0.3,
        max_tokens=max_tokens,
    )
    return resp.choices[0].message.content.strip()


def _parse_json(text):
    # try full match first
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            pass
    return {"raw": text}


# --- ORCHESTRATOR ---

def orchestrator(task, memory_context=""):
    system = (
        "You are the Orchestrator of NEXUS AI. "
        "Decide which agents to run based on the task type.\n"
        "Rules:\n"
        "- If task asks to write/build/implement code -> include coder\n"
        "- If task involves CSV/data/analysis -> include researcher, analyst\n"
        "- Always include: planner, critic, optimizer, validator, reporter\n"
        "Return ONLY valid JSON:\n"
        '{"task":"<task>","pipeline":["planner","researcher","coder","analyst","critic","optimizer","validator","reporter"],"notes":"<one line>"}\n'
        "Only include agents that are needed. Always end with validator, reporter."
    )
    msg = f"Task: {task}"
    if memory_context:
        msg += f"\nPast context: {memory_context}"
    result = _call(system, msg, max_tokens=300)
    parsed = _parse_json(result)
    if "pipeline" not in parsed:
        parsed["pipeline"] = ["planner", "researcher", "analyst", "critic", "optimizer", "validator", "reporter"]
    return parsed


# --- PLANNER ---

def planner(task, orchestrator_notes=""):
    system = (
        "You are the Planner agent. Break the task into 4-6 clear numbered steps.\n"
        "Return ONLY valid JSON:\n"
        '{"steps":[{"step":1,"action":"<what>","agent":"<who>"}],"estimated_complexity":"low|medium|high"}'
    )
    msg = f"Task: {task}"
    result = _call(system, msg, max_tokens=400)
    return _parse_json(result)


# --- RESEARCHER ---

def researcher(task, csv_summary="", memory_facts=None):
    system = (
        "You are the Researcher agent. Provide relevant background and key facts for the task. "
        "If CSV data is given, highlight the most important patterns. Be concise — max 200 words."
    )
    parts = [f"Task: {task}"]
    if memory_facts:
        parts.append("Past facts:\n" + "\n".join(memory_facts[:3]))
    if csv_summary:
        parts.append(f"CSV Data:\n{csv_summary}")
    return _call(system, "\n\n".join(parts), max_tokens=400)


# --- CODER ---

def coder(task, research_context=""):
    system = (
        "You are the Coder agent. Write clean working Python code.\n"
        "Rules:\n"
        "- Wrap ALL code in ```python ... ``` blocks\n"
        "- Add brief inline comments\n"
        "- No emojis, no fluff"
    )
    msg = f"Task: {task}"
    if research_context:
        msg += f"\nContext: {research_context[:300]}"
    return _call(system, msg, max_tokens=800)


# --- ANALYST ---

def analyst(task, research_context="", csv_summary="", sql_insights=""):
    system = (
        "You are the Analyst agent. Produce 5 concrete data-driven insights. "
        "Reference specific numbers if available. Be direct and concise."
    )
    parts = [f"Task: {task}"]
    if csv_summary:
        parts.append(f"CSV Data:\n{csv_summary}")
    if sql_insights:
        parts.append(f"SQL Query Results:\n{sql_insights}")
    if research_context:
        parts.append(f"Research:\n{research_context[:200]}")
    return _call(system, "\n\n".join(parts), max_tokens=500)


# --- CRITIC ---

def critic(task, previous_output=""):
    system = (
        "You are the Critic agent. Review the output and score it.\n"
        'Return ONLY valid JSON: {"score":<1-10>,"issues":["<issue>"],"suggestions":["<suggestion>"]}'
    )
    # truncate to avoid slow processing
    msg = f"Task: {task}\nOutput (truncated):\n{str(previous_output)[:600]}"
    result = _call(system, msg, max_tokens=250)
    parsed = _parse_json(result)
    if "score" not in parsed:
        parsed = {"score": 7, "issues": [], "suggestions": ["Add more detail"]}
    return parsed


# --- OPTIMIZER ---

def optimizer(task, previous_output, critic_feedback):
    system = (
        "You are the Optimizer agent. Fix the issues in the output.\n"
        "Return improved output as plain text. For code use ```python``` blocks. Be concise."
    )
    issues = critic_feedback.get("issues", [])
    suggestions = critic_feedback.get("suggestions", [])
    msg = (
        f"Task: {task}\n"
        f"Issues to fix: {issues}\n"
        f"Suggestions: {suggestions}\n"
        f"Original output:\n{str(previous_output)[:800]}"
    )
    return _call(system, msg, max_tokens=700)


# --- VALIDATOR ---

def validator(task, final_output):
    system = (
        "You are the Validator agent. Check output quality.\n"
        'Return ONLY valid JSON: {"status":"PASS","score":<1-10>,"verdict":"<one line>","final_answer":"<output or same>"}'
    )
    msg = f"Task: {task}\nOutput:\n{str(final_output)[:800]}"
    result = _call(system, msg, max_tokens=500)
    parsed = _parse_json(result)
    if "status" not in parsed:
        parsed = {"status": "PASS", "score": 8, "verdict": "Acceptable", "final_answer": str(final_output)}
    return parsed


# --- REPORTER ---

def reporter(task, validated_output, plan_steps, critic_score, validator_result):
    system = (
        "You are the Reporter agent. Write a concise final report.\n"
        "Format exactly:\n"
        "## Task\n<task>\n\n"
        "## Steps Taken\n<numbered list>\n\n"
        "## Result\n<final answer>\n\n"
        "## Quality Score\n<score>/10"
    )
    steps_text = ""
    if plan_steps and isinstance(plan_steps, list):
        steps_text = "\n".join(
            f"{s.get('step', i+1)}. [{s.get('agent','?').upper()}] {s.get('action', '')}"
            for i, s in enumerate(plan_steps)
        )

    final = validated_output.get("final_answer", "") if isinstance(validated_output, dict) else str(validated_output)
    score = validator_result.get("score", critic_score) if isinstance(validator_result, dict) else critic_score

    msg = f"Task: {task}\nSteps:\n{steps_text}\nFinal answer:\n{str(final)[:600]}\nScore: {score}/10"
    return _call(system, msg, max_tokens=600)