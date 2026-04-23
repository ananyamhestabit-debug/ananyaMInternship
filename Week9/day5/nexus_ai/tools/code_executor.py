import io
import os
import contextlib


def execute_code(code: str) -> str:
    """Execute a Python code string and return its stdout output."""
    output = io.StringIO()
    try:
        with contextlib.redirect_stdout(output):
            exec(code, {})
        result = output.getvalue()
        return result if result else "Code executed successfully (no output)"
    except Exception as e:
        return f"Execution Error: {e}"
