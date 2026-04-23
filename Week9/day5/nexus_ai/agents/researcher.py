from .base import create_agent

def create_researcher():
    return create_agent(
        "researcher",
        """
You generate the actual answer.

- Solve the user’s request directly
- Be clear and structured
- Do NOT analyze or critique the answer
"""
    )