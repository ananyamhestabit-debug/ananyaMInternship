from .base import create_agent

def create_critic():
    return create_agent(
        "critic",
        """
You are a Critic.

Your job:
- Only fix small issues
- Do NOT rewrite entire answer
- Do NOT turn answer into analysis

If answer is good → return same answer
"""
    )