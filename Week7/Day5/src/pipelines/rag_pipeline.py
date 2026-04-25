from generator.llm_client import LLMClient
from pipelines.context_builder import build_context, get_relevant_snippet
from sentence_transformers import SentenceTransformer
from utils.prompt_loader import load_prompt

model = SentenceTransformer("all-MiniLM-L6-v2")
llm = LLMClient()


def generate_answer(question, memory_context, chunks_file="data/chunks/chunks.json"):

    chunks = build_context(chunks_file, question, top_k=5)

    context_list = []
    context_text = ""

    for c in chunks:
        snippet = get_relevant_snippet(question, c["content"], model)

        context_list.append({
            "chunk_id": c["chunk_id"],
            "content": snippet,
            "metadata": c["metadata"]
        })

        context_text += snippet + "\n"

    base_prompt = load_prompt("rag_prompt.txt")

    prompt = f"""
{base_prompt}

Context:
{context_text}

Memory:
{memory_context}

Question:
{question}
"""

    answer = llm.generate(prompt)

    return answer, context_list