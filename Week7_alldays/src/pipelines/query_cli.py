from retriever.query_engine import QueryEngine


def main():
    print("=" * 50)
    print("Enterprise RAG System - Day 1")
    print("=" * 50)

    qe = QueryEngine()

    while True:
        query = input("\nEnter query (or 'exit'): ")

        if query.lower() == "exit":
            print("Exiting...")
            break

        results = qe.query(query)

        print("\nResults:\n")

        for i, r in enumerate(results):
            print(f"Result {i+1}")
            print(f"Source: {r['source']} (Page {r['page']})")
            print(f"Score: {r['score']}")
            print(f"Text: {r['text']}")
            print("-" * 50)


if __name__ == "__main__":
    main()