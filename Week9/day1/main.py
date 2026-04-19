import logging
import uuid
from agents.research_agent import create_research_agent
from agents.summarizer_agent import create_summarizer_agent
from agents.answer_agent import create_answer_agent

# -----------------------------
# LOGGING CONFIG (CLEAN)
# -----------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

# Hide noisy HTTP logs
logging.getLogger("httpx").setLevel(logging.WARNING)


def run_pipeline(query: str):
    request_id = str(uuid.uuid4())[:6]

    logging.info(f"[{request_id}] 🚀 Pipeline started")
    logging.info(f"[{request_id}] Query: {query}")

    # Initialize agents
    research_agent = create_research_agent()
    summarizer_agent = create_summarizer_agent()
    answer_agent = create_answer_agent()

    try:
        # -----------------------------
        # STEP 1 — RESEARCH
        # -----------------------------
        logging.info(f"[{request_id}] 🔍 Research phase")

        research_output = research_agent.generate_reply(
            messages=[{
                "role": "user",
                "content": query
            }]
        )

        if not research_output:
            raise ValueError("Empty research output")

        # -----------------------------
        # STEP 2 — SUMMARIZATION
        # -----------------------------
        logging.info(f"[{request_id}] 📝 Summarization phase")

        summary = summarizer_agent.generate_reply(
            messages=[{
                "role": "user",
                "content": research_output
            }]
        )

        if not summary:
            raise ValueError("Empty summary output")

        # -----------------------------
        # STEP 3 — FINAL ANSWER
        # -----------------------------
        logging.info(f"[{request_id}] ✅ Answer generation phase")

        final_answer = answer_agent.generate_reply(
            messages=[{
                "role": "user",
                "content": f"""
Convert the following into a clean structured answer.

STRICT FORMAT:

Title: AI in Healthcare

1. Introduction
(2-3 lines)

2. Key Applications
- Bullet points

3. Real-World Use Cases
- Example with explanation

4. Benefits
- Bullet points

5. Conclusion
(Short and impactful)

CONTENT:
{summary}

IMPORTANT RULES:
- No repetition
- Fix grammar
- No conversational tone
- No extra text
- Maintain consistent bullet formatting
- Do not add extra spaces before bullets
- Use only verified real-world examples

CONCLUSION RULE:
End with a strong, impactful closing line highlighting the future importance of AI in healthcare.
"""
            }]
        )

        if not final_answer:
            raise ValueError("Empty final answer")

        logging.info(f"[{request_id}] 🎯 Pipeline completed successfully")

        return final_answer

    except Exception as e:
        logging.error(f"[{request_id}] ❌ Error: {str(e)}")
        return "Error occurred during processing."


# -----------------------------
# ENTRY POINT
# -----------------------------
if __name__ == "__main__":
    query = "Explain AI in healthcare with real-world use cases"

    result = run_pipeline(query)

    print("\n" + "=" * 60)
    print("FINAL OUTPUT:\n")
    print(result)
    print("=" * 60)