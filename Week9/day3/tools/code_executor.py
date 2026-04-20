"""
DAY 3 — Code Executor Agent
Tool: Generate Python code and execute it safely using subprocess
"""

import subprocess
import tempfile
import os
import re
import time
from groq import Groq

client = Groq()

CODE_AGENT_PROMPT = """You are the Code Agent in a multi-agent AI system.

Your ONLY job: Write Python code to solve the given task, then the code will be executed.

Rules:
- Write ONLY pure Python code (no bash, no shell commands)
- Use only standard library + pandas + csv modules (always available)
- Your code must PRINT its results — use print() for all output
- Keep code simple and focused
- Handle errors with try/except
- Do NOT use matplotlib, seaborn or any visualization library
- Do NOT use external APIs

Return ONLY a Python code block like this:
```python
# your code here
print("result")
```

No explanation before or after. Just the code block."""


def extract_code(text: str) -> str:
    """Extracts Python code from markdown code block"""
    match = re.search(r'```python\n(.*?)```', text, re.DOTALL)
    if match:
        return match.group(1).strip()
    # If no markdown block, try to use raw text as code
    return text.strip()


def execute_python(code: str, timeout: int = 15) -> dict:
    """
    Executes Python code in a subprocess safely.
    Returns dict with stdout, stderr, success status.
    """
    # Write code to a temp file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write(code)
        tmp_path = f.name

    try:
        result = subprocess.run(
            ["python3", tmp_path],
            capture_output=True,
            text=True,
            timeout=timeout
        )
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout.strip(),
            "stderr": result.stderr.strip(),
            "code": code
        }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "stdout": "",
            "stderr": f"Code execution timed out after {timeout}s",
            "code": code
        }
    finally:
        os.unlink(tmp_path)


def run_code_agent(instruction: str, context: str = "") -> dict:
    """
    Generates Python code for the instruction, executes it,
    returns the execution result.
    """
    print(f"\n[CODE AGENT] Instruction: {instruction[:80]}...")

    user_message = instruction
    if context:
        user_message += f"\n\nContext/Data available:\n{context}"

    # Step 1: Generate code
    time.sleep(2)  # rate limit buffer
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": CODE_AGENT_PROMPT},
            {"role": "user", "content": user_message}
        ],
        temperature=0.2,
        max_tokens=800
    )

    raw_response = response.choices[0].message.content.strip()
    code = extract_code(raw_response)

    print(f"[CODE AGENT] Code generated ({len(code)} chars)")
    print(f"[CODE AGENT] Executing code...")

    # Step 2: Execute code
    exec_result = execute_python(code)

    if exec_result["success"]:
        print(f"[CODE AGENT] Execution successful ✓")
        output = f"💻 CODE EXECUTED SUCCESSFULLY:\n\n```python\n{code}\n```\n\n📤 OUTPUT:\n{exec_result['stdout']}"
    else:
        print(f"[CODE AGENT] Execution failed — returning generated code")
        output = f"💻 GENERATED CODE:\n\n```python\n{code}\n```\n\n⚠️ Execution note: {exec_result['stderr'][:200]}"

    return {
        "agent": "code_agent",
        "instruction": instruction,
        "code": code,
        "execution": exec_result,
        "output": output
    }


if __name__ == "__main__":
    result = run_code_agent(
        instruction="Write Python code to calculate the sum of numbers 1 to 100 and print the result"
    )
    print(result["output"])
