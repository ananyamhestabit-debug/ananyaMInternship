from orchestrator.nexus import NexusAI

# ── Entry point for NEXUS AI ──────────────────────────────────────
def main():
    print("\nNEXUS AI is starting...\n")
    nexus = NexusAI()

    while True:
        try:
            user_input = input("You: ")

            if user_input.lower() in ["exit", "quit"]:
                print("Goodbye!")
                break

            nexus.run(user_input)

        except KeyboardInterrupt:
            print("\nSession ended.")
            break

if __name__ == "__main__":
    main()