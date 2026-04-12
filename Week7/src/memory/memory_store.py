from collections import deque

class MemoryStore:
    def __init__(self, k=5):
        # buffer stores last k conversations
        self.buffer = deque(maxlen=k)

    def add(self, question, answer):
        # add new interaction
        self.buffer.append({
            "q": question,
            "a": answer
        })

    def get(self):
        # return memory as formatted string (for LLM prompt)
        if not self.buffer:
            return ""

        memory_text = ""

        for m in self.buffer:
            memory_text += f"Q: {m['q']}\nA: {m['a']}\n"

        return memory_text

    def get_all(self):
        # return raw list (for UI display)
        return list(self.buffer)

    def clear(self):
        # clear all memory
        self.buffer.clear()