from generator.llm_client import LLMClient
from pipelines.context_builder import build_context, get_relevant_snippet
from sentence_transformers import SentenceTransformer
from utils.prompt_loader import load_prompt

model = SentenceTransformer("all-MiniLM-L6-v2")
llm = LLMClient()

CHUNKS_FILE = "data/chunks/chunks.json"


def generate_answer(question, memory_context):
    chunks = build_context(CHUNKS_FILE, question, top_k=5)

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

    if len(answer) < 20:
        answer += " (refined: insufficient detail)"

    return answer, context_list


if __name__ == "__main__":
    print("RAG CLI Mode Started\n")

    memory = ""

    while True:
        q = input("Enter your question (type exit to quit): ")

        if q.lower() == "exit":
            break

        answer, context = generate_answer(q, memory)

        print("\nAnswer:\n")
        print(answer)

        print("\nTop Context:\n")
        for i, c in enumerate(context):
            print(f"Result {i+1}")
            print(c["content"][:200])
            print("-" * 40)

        memory += f"\nQ:{q}\nA:{answer}"