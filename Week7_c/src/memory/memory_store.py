memory = []

def add_to_memory(query, response):
    memory.append({
        "query": query,
        "response": str(response)[:200]
    })

    # keep only last 5
    if len(memory) > 5:
        memory.pop(0)

def get_memory():
    return memory