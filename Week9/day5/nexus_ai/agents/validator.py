from .base import create_agent

def create_validator():
    return create_agent(
        "validator",
        """
You are a Validator.

- Check correctness
- Fix errors
- Return final answer only
"""
    )