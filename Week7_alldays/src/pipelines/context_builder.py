def build_context(docs, max_chars=1500):
    context = ""
    used = []

    for d in docs:
        text = d["text"]

        # skip very large chunks
        if len(text) > max_chars:
            text = text[:500]

        if len(context) + len(text) > max_chars:
            continue   # IMPORTANT: break nahi, continue

        context += text + "\n\n"
        used.append(d)

    return context, used