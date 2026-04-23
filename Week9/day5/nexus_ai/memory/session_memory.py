class SessionMemory:
    def __init__(self, max_turns=6):
        self.history = []
        self.max_turns = max_turns

    def add_message(self, role, content):
        self.history.append({"role": role, "content": content})

        if len(self.history) > self.max_turns:
            self.history.pop(0)

    def get_context(self):
        context = ""
        for msg in self.history:
            context += f"{msg['role']}: {msg['content']}\n"
        return context.strip()