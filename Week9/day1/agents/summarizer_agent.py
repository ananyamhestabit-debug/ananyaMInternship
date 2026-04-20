from autogen import AssistantAgent
from config import get_llm_config

def create_summarizer_agent():
    return AssistantAgent(
        name="SummarizerAgent",
        llm_config=get_llm_config(),
        system_message="""
ROLE: Summarizer Agent

TASK:
Convert research into clean structured summary.

STRICT RULES:
- Remove duplicates
- Remove weak/generic points
- Keep only strong insights
- No repetition
- No meta text

OUTPUT:
Clean structured summary
"""
    )