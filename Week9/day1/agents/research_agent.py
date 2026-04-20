from autogen import AssistantAgent
from config import get_llm_config

def create_research_agent():
    return AssistantAgent(
        name="ResearchAgent",
        llm_config=get_llm_config(),
        system_message="""
ROLE: Research Agent

TASK:
Provide detailed factual research about the query.

STRICT RULES:
- No summarization
- No repetition
- No explanation fluff
- Only factual structured data

REQUIREMENTS:
- Include real-world systems/tools
- Mention AI techniques used (ML, NLP, CV)
- Explain HOW system works briefly

OUTPUT:
- Bullet points
- Structured factual information
"""
    )