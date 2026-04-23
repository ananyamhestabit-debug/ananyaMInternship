from llm import call_llm

class SummarizerAgent:
    def __init__(self):

        #separation of concerns: make ouput readable and not waste token, filtering logic(impt facts, high value info, key points, same lien is removed), duplicate removal but stricter(like same idea is removed) 
        self.system_prompt = """
ROLE: Summarizer Agent

TASK:
Convert research into clean summary.

RULES:
- Remove duplicates
- Keep strong insights only
- No repetition
"""

    def run(self, messages):
        messages = [{"role": "system", "content": self.system_prompt}] + messages
        return call_llm(messages)