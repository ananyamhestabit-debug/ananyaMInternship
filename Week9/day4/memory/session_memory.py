"""
DAY 4 - Session Memory (Short-term)
Stores conversation turns in memory for the current session only.
Cleared when the program exits.
"""


class SessionMemory:
    def __init__(self, max_turns=10):
        self.max_turns = max_turns
        self.turns = []  # list of {role, content}

    def add(self, role: str, content: str):
        self.turns.append({"role": role, "content": content})
        # keep only last max_turns
        if len(self.turns) > self.max_turns:
            self.turns = self.turns[-self.max_turns:]

    def get_history(self) -> list:
        return self.turns

    def clear(self):
        self.turns = []

    def summary(self) -> str:
        return f"Session memory: {len(self.turns)} turns stored"
