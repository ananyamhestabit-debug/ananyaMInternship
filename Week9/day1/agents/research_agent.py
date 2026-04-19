from autogen import AssistantAgent
from config import get_llm_config

def create_research_agent():
    return AssistantAgent(
        name="ResearchAgent",
        llm_config=get_llm_config(),
        system_message="""
ROLE: Research Agent

TASK:
Provide detailed factual research.

STRICT RULES:
- No summarization
- No instructions
- No repetition
- Only facts

OUTPUT FORMAT:
- Bullet points
- Clean structured data
""",
        max_consecutive_auto_reply=10,
    )