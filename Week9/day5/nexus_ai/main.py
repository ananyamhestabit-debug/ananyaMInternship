from orchestrator.nexus import NexusAI

def main():

    system = NexusAI()

    while True:
        try:
            q = input("\nUser: ")

            if q.lower() in ["exit", "quit"]:
                break

            
            system.run(q)


        except KeyboardInterrupt:
            print("\nExiting...")
            break


if __name__ == "__main__":
    main()