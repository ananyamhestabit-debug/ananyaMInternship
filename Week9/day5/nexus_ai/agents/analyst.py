from .base import create_agent

def create_analyst():
    return create_agent(
        "analyst",
        """
You analyze content.

- Extract insights, comparisons, patterns
- Do NOT rewrite or replace original answer
"""
    )