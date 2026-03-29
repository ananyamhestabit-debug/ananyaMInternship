from src.pipelines.final_pipeline import final_system

def run():

    print("=== MULTIMODAL RAG SYSTEM ===")

    while True:
        query = input("\nEnter query (type 'exit' to quit): ")

        if query.lower() == "exit":
            break

        result = final_system(query)

        print("\n=== RESPONSE ===")
        print(result["response"])

        print("\n=== EVALUATION ===")
        print(result["evaluation"])

        print("\n=== HALLUCINATION ===")
        print(result["hallucination"])


if __name__ == "__main__":
    run()