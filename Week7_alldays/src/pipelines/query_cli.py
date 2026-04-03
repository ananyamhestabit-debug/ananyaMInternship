from retriever.hybrid_retriever import HybridRetriever
from pipelines.context_builder import build_context


def main():
    print("-" * 50)
    print("Enterprise RAG System - Day 2 (Hybrid)")
    print("-" * 50)

    retriever = HybridRetriever()

    while True:
        query = input("\nEnter query (or 'exit'): ")

        if query.lower() == "exit":
            print("Exiting...")
            break

        # Step 1: retrieve documents
        results = retriever.query(query)

        # Step 2: show ALL retrieved results
        print("\nTop Retrieved Chunks:\n")

        for i, r in enumerate(results):
            print(f"Result {i+1}")
            print(f"Source: {r['source']} (Page {r['page']})")
            print(f"Type: {r.get('type', 'pdf')}")
            print(f"Text: {r['text'][:300]}")
            print("-" * 50)

        # Step 3: build context separately
        context, used_docs = build_context(results)

        print("\n===== FINAL CONTEXT (for LLM) =====\n")
        print(context[:1500])
        print("\n==================================\n")


if __name__ == "__main__":
    main()