from autogen import AssistantAgent
from config import get_llm_config

def create_summarizer_agent():
    return AssistantAgent(
        name="SummarizerAgent",
        llm_config=get_llm_config(),
        system_message="""
ROLE: Summarizer Agent

TASK:
Convert research into clean, non-repetitive summary.

STRICT RULES:
- Remove duplicates
- Keep only meaningful insights
- No instructions
- No meta text
- No repetition

OUTPUT:
Clean structured summary only
""",
        max_consecutive_auto_reply=10,
    )