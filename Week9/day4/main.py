"""
DAY 4 - Main Runner
Memory System: session + long-term + vector
"""

import os
import sys
sys.path.insert(0, os.path.dirname(__file__))

from agents.memory_agent import chat, session
from memory import long_term_memory as ltm
from memory import vector_store as vs


def show_memory_status():
    facts = ltm.get_all_memories(memory_type="fact")
    store = vs.load_store()
    print(f"\n--- Memory Status ---")
    print(f"Session turns     : {len(session.get_history())}")
    print(f"Long-term facts   : {len(facts)}")
    print(f"Vector store size : {len(store.get('texts', []))}")
    print("---------------------\n")


def show_long_term():
    facts = ltm.get_all_memories()
    if not facts:
        print("No long-term memories yet.")
        return
    print("\n--- Long-term Memories ---")
    for f in facts:
        print(f"[{f['id']}] {f['type']} | {f['content']}")
    print("--------------------------\n")


def main():
    print("Day 4 - Memory Agent")
    print("Commands: 'status', 'memory', 'clear', 'quit'")
    print("Anything else is treated as a query.\n")

    # demo: pre-load a couple of facts so memory recall is visible
    ltm.save_memory("User is learning about AI and multi-agent systems", memory_type="fact")
    vs.add_to_vector_store("User is interested in Python and AI development")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nExiting.")
            break

        if not user_input:
            continue

        if user_input.lower() == "quit":
            break
        elif user_input.lower() == "status":
            show_memory_status()
        elif user_input.lower() == "memory":
            show_long_term()
        elif user_input.lower() == "clear":
            ltm.clear_all()
            vs.clear_vector_store()
            session.clear()
            print("All memory cleared.")
        else:
            chat(user_input)


if __name__ == "__main__":
    main()
