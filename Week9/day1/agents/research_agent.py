from llm import call_llm   #agent does not think by itself it uses llm to think

class ResearchAgent:
    def __init__(self):

        #no overlap with summarizer agent, removes unnecesary words, forces bullet point sadn orgranized data, answer must include ml, nlp, comp vision
        self.system_prompt = """
ROLE: Research Agent

TASK:
Provide detailed factual research.

RULES:
- No summarization
- No fluff
- Only structured facts
- Include ML/NLP/CV usage
- Mention real systems
"""

    def run(self, messages):
        messages = [{"role": "system", "content": self.system_prompt}] + messages
        return call_llm(messages)