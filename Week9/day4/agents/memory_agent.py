"""
DAY 4 - Memory Agent
Uses session memory, long-term memory, and vector memory together.
Flow: new query -> search vector memory -> fetch long-term facts -> inject context -> generate answer
"""

import time
from groq import Groq
from memory.session_memory import SessionMemory
from memory import long_term_memory as ltm
from memory import vector_store as vs

client = Groq()
session = SessionMemory(max_turns=10)

SYSTEM_PROMPT = """You are a helpful AI assistant with memory.
You will be given context from past conversations and facts when relevant.
Use this context to give better, more personalized answers.
Be concise and direct."""


def extract_facts(query: str, response: str) -> str:
    # Ask the model to extract a one-line fact worth remembering
    result = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "user",
                "content": f"Extract one important fact from this exchange worth remembering long-term. Return ONLY the fact as a single sentence, nothing else.\n\nUser said: {query}\nAssistant said: {response[:300]}"
            }
        ],
        temperature=0.1,
        max_tokens=100
    )
    return result.choices[0].message.content.strip()


def chat(user_query: str) -> str:
    print(f"\n[USER] {user_query}")

    # Step 1: search vector memory for similar past context
    similar = vs.search_similar(user_query, top_k=2)
    vector_context = ""
    if similar:
        print(f"[MEMORY] Found {len(similar)} similar memories")
        vector_context = "Relevant past context:\n"
        for s in similar:
            vector_context += f"- {s['text']}\n"

    # Step 2: fetch recent long-term facts
    long_term_facts = ltm.get_all_memories(memory_type="fact")
    fact_context = ""
    if long_term_facts:
        recent_facts = long_term_facts[:5]
        fact_context = "Known facts about user:\n"
        for f in recent_facts:
            fact_context += f"- {f['content']}\n"

    # Step 3: build messages with injected context
    system_with_context = SYSTEM_PROMPT
    if vector_context or fact_context:
        system_with_context += f"\n\n{vector_context}\n{fact_context}"

    messages = [{"role": "system", "content": system_with_context}]

    # add session history
    for turn in session.get_history():
        messages.append(turn)

    # add current query
    messages.append({"role": "user", "content": user_query})

    # Step 4: generate response
    time.sleep(1)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages,
        temperature=0.5,
        max_tokens=600
    )

    answer = response.choices[0].message.content.strip()
    print(f"[AGENT] {answer}")

    # Step 5: update session memory
    session.add("user", user_query)
    session.add("assistant", answer)

    # Step 6: extract and store fact in long-term memory
    time.sleep(1)
    fact = extract_facts(user_query, answer)
    ltm.save_memory(fact, memory_type="fact")
    print(f"[MEMORY] Stored fact: {fact}")

    # Step 7: store full exchange in vector memory for future similarity search
    exchange = f"User asked: {user_query} | Assistant answered: {answer[:200]}"
    vs.add_to_vector_store(exchange)

    return answer
