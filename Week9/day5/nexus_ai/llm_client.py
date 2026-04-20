import time
from groq import Groq
from nexus_ai.config import GROQ_MODEL, AGENT_SLEEP

client = Groq()

def call_llm(system: str, user: str, max_tokens: int = 800, temperature: float = 0.3) -> str:
    time.sleep(AGENT_SLEEP)
    res = client.chat.completions.create(
        model=GROQ_MODEL,
        messages=[{"role": "system", "content": system}, {"role": "user", "content": user}],
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return res.choices[0].message.content.strip()
