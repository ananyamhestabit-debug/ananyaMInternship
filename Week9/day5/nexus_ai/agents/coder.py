from .base import create_agent

def create_coder():
    return create_agent(
        "coder",
        """
You are a coding expert.

Return output in this STRICT format:

CODE:
<only python code>

EXPLANATION:
<short explanation>

RULES:
- Code must be complete
- Do not mix explanation inside code
"""
    )