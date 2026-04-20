"""
output_saver.py

Decision logic — based ONLY on task/query text, never on generated content:
  - Task has code keywords (write/build/implement/api/script etc.) -> code query
  - Everything else (analyze/plan/design/strategy/generate report) -> NOT code query

Code query  -> save .py (extracted code) + .md (report)
Other query -> no file saved, CLI output only
"""

import os, re
from nexus_ai.config import OUTPUT_DIR

os.makedirs(OUTPUT_DIR, exist_ok=True)

# Keywords that mean the USER explicitly wants code written
CODE_KEYWORDS = [
    "write", "build", "implement", "code", "script", "function", "class",
    "api", "backend", "fastapi", "flask", "django", "program",
    "ml pipeline", "machine learning pipeline", "rag pipeline",
    "generate code", "create an api", "create a script",
]

# These words OVERRIDE code keywords — query is NOT a code task even if code appears in output
NON_CODE_OVERRIDES = [
    "analyze", "analysis", "strategy", "plan", "report",
    "design", "compare", "evaluate", "suggest", "recommend",
    "create a business", "business strategy",
]


def _is_code_task(task: str) -> bool:
    """
    Checks only the task string — never the generated output.
    Non-code overrides take priority over code keywords.
    """
    t = task.lower()
    # if the query is clearly analytical/strategic, it's not a code task
    if any(kw in t for kw in NON_CODE_OVERRIDES):
        return False
    # only then check for explicit code keywords
    return any(kw in t for kw in CODE_KEYWORDS)


def _extract_code(text: str) -> str:
    """Pull Python code blocks out of markdown. Returns only the code."""
    blocks = re.findall(r'```(?:python)?\n(.*?)```', text, re.DOTALL)
    if blocks:
        parts = []
        for i, block in enumerate(blocks, 1):
            parts.append(f"# --- Block {i} ---\n{block.strip()}")
        return "\n\n".join(parts)
    # no fenced blocks found — return raw text as-is
    return text


def save_py(task: str, code_text: str, timestamp: str) -> str:
    """Save extracted code to a .py file. Returns filepath."""
    filename = f"output_{timestamp}.py"
    filepath = os.path.join(OUTPUT_DIR, filename)
    code_body = _extract_code(code_text)
    content = "\n".join([
        '"""',
        f"NEXUS AI - Generated Code",
        f"Task      : {task}",
        f"Generated : {timestamp}",
        '"""',
        "",
        code_body,
    ])
    with open(filepath, "w") as f:
        f.write(content)
    return filepath


def save_md(task: str, report: str, timestamp: str, suffix: str = "") -> str:
    """Save report to a .md file. Returns filepath."""
    filename = f"output_{timestamp}{suffix}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)
    content = "\n".join([
        "# NEXUS AI — Output Report",
        "",
        f"**Task:** {task}  ",
        f"**Generated:** {timestamp}",
        "",
        "---",
        "",
        report,
    ])
    with open(filepath, "w") as f:
        f.write(content)
    return filepath
