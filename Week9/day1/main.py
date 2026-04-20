import logging
import uuid

from agents.research_agent import create_research_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.answer_agent import create_answer_agent

from cache import get_cached_response, set_cached_response


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logging.getLogger("httpx").setLevel(logging.WARNING)


def run_pipeline(query: str):
    request_id = str(uuid.uuid4())[:6]

    logging.info(f"[{request_id}]  Pipeline started")
    logging.info(f"[{request_id}] Query: {query}")

    # ---------------- CACHE ----------------
    cached = get_cached_response(query)
    if cached:
        logging.info(f"[{request_id}] ⚡ Cache hit")
        return cached

    # ---------------- AGENTS ----------------
    research_agent = create_research_agent()
    summarizer_agent = create_summarizer_agent()
    answer_agent = create_answer_agent()

    try:
        # STEP 1 — RESEARCH
        logging.info(f"[{request_id}]  Research phase")

        research = research_agent.generate_reply(
            messages=[{"role": "user", "content": query}]
        )

        # STEP 2 — SUMMARY
        logging.info(f"[{request_id}]  Summarization phase")

        summary = summarizer_agent.generate_reply(
            messages=[{"role": "user", "content": research}]
        )

        # STEP 3 — FINAL ANSWER (FIXED PROMPT)
        logging.info(f"[{request_id}]  Answer generation phase")

        final = answer_agent.generate_reply(
            messages=[{
                "role": "user",
                "content": f"""
Transform into structured answer.

STRICT FORMAT:

Title: AI in Healthcare

1. Introduction
(2-3 lines with ML/NLP/CV)

2. Key Applications (WHAT + HOW)
- Max 5 points

3. Real-World Use Cases (WHAT + HOW + IMPACT)

4. Benefits

5. Conclusion

CONTENT:
{summary}

STRICT RULES:
- Do NOT skip any section
- Do NOT output only use cases
- No generic lines
- Maintain proper structure
"""
            }]
        )

        # SAVE CACHE
        set_cached_response(query, final)

        logging.info(f"[{request_id}] Pipeline completed")

        return final

    except Exception as e:
        logging.error(f"[{request_id}]  Error: {str(e)}")
        return "Error occurred"


# ENTRY POINT
if __name__ == "__main__":
    query = "Explain AI in healthcare with real-world use cases"

    output = run_pipeline(query)

    print("\n" + "=" * 60)
    print("FINAL OUTPUT:\n")
    print(output)
    print("=" * 60)