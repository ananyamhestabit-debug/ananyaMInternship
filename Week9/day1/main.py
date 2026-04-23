import logging
import uuid

from agents.research_agent import ResearchAgent
from agents.summarizer_agent import SummarizerAgent
from agents.answer_agent import AnswerAgent

from cache import get_cached_response, set_cached_response

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# MEMORY
conversation_memory = []
MEMORY_WINDOW = 10


def update_memory(msg):
    global conversation_memory

    conversation_memory.append(msg)

    if len(conversation_memory) > MEMORY_WINDOW:
        conversation_memory = conversation_memory[-MEMORY_WINDOW:]


def run_pipeline(query):
    request_id = str(uuid.uuid4())[:6]

    logging.info(f"[{request_id}] START")
    logging.info(f"Query: {query}")

    cached = get_cached_response(query)
    if cached:
        logging.info("Cache hit")
        return cached

    research_agent = ResearchAgent()
    summarizer_agent = SummarizerAgent()
    answer_agent = AnswerAgent()

    try:
        # STEP 1
        update_memory({"role": "user", "content": query})

        research = research_agent.run(conversation_memory)
        update_memory({"role": "assistant", "content": research})

        # STEP 2
        update_memory({"role": "user", "content": research})

        summary = summarizer_agent.run(conversation_memory)
        update_memory({"role": "assistant", "content": summary})

        # STEP 3
        final_prompt = f"""
Convert into structured answer:

{summary}

FORMAT:
1. Introduction
2. Key Applications
3. Use Cases
4. Benefits
5. Conclusion
"""

        update_memory({"role": "user", "content": final_prompt})

        final = answer_agent.run(conversation_memory)
        update_memory({"role": "assistant", "content": final})

        set_cached_response(query, final)

        logging.info(f"[{request_id}] DONE")

        return final

    except Exception as e:
        logging.error(str(e))
        return "Error occurred"


if __name__ == "__main__":
    query = "Explain AI in healthcare with real-world use cases"
    result = run_pipeline(query)

    print("\n" + "="*60)
    print(result)
    print("="*60)