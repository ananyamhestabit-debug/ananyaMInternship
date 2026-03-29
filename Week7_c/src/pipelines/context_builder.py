def build_context(results, top_k=5):
    seen = set()
    final = []

    for r in results:
        key = (r["source"], r["chunk_id"])
        if key not in seen:
            final.append(r)
            seen.add(key)

    return final[:top_k]