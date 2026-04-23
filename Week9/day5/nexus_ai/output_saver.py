import re
import time
from nexus_ai.config import OUTPUT_DIR

# These words in task = definitely a code task
CODE_TRIGGERS = [
    "write a", "write python", "build a", "build python", "implement",
    "create a script", "create a function", "create a class",
    "fastapi", "rest api", "crud", "flask", "django",
    "python code", "python script", "code for", "program to",
]

# These words override even if code keywords present (pure analysis/plan tasks)
NON_CODE_PURE = [
    "analyze", "analysis", "business strategy", "plan a startup",
    "design architecture", "rag pipeline", "explain", "compare", "recommend",
]


def _is_code_task(task_text):
    t = task_text.lower()
    # if clearly a non-code task, skip
    for phrase in NON_CODE_PURE:
        if phrase in t:
            return False
    # if any code trigger present, it's a code task
    for phrase in CODE_TRIGGERS:
        if phrase in t:
            return True
    return False


def _extract_code(text):
    matches = re.findall(r"```python(.*?)```", text, re.DOTALL)
    return "\n\n".join(m.strip() for m in matches) if matches else None


def save_output(task, content):
    ts = int(time.time())
    code = _extract_code(str(content))

    # Save .py if: task is code task AND there's actual code in the output
    if code and _is_code_task(task):
        py_path = OUTPUT_DIR / f"output_{ts}.py"
        md_path = OUTPUT_DIR / f"output_{ts}_report.md"
        py_path.write_text(code, encoding="utf-8")
        md_path.write_text(f"# Report\n\n**Task:** {task}\n\n{content}", encoding="utf-8")
        return str(py_path), str(md_path)

    return None, None