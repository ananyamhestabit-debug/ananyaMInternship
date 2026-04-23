from .base import create_agent

def create_optimizer():
    return create_agent(
        "optimizer",
        """
You improve clarity.

- Make output concise and structured
- Do NOT change meaning
"""
    )