from llm import call_llm

class AnswerAgent:  #class for reusability and encapsulation of role, prompt, and behavior
    def __init__(self):

        #not a general agent but only an ans agent:strict system prompts that constrain behavior
        #-prevent hallucination
        #-force dependency on summarizer output
        #-ensures formatted output 
#role and limitations
        self.system_prompt = """
ROLE: Answer Agent      

TASK:
Convert summary into structured answer.

RULES:
- Do NOT add new info
- Use only given content 
- Maintain structure
"""

    def run(self, messages):
        messages = [{"role": "system", "content": self.system_prompt}] + messages  #chat format for llm:first system prompts then conversation as llm reads top to bottom : first system instruction then agent/user messages
        return call_llm(messages)