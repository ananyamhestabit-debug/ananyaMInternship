def chunk_text(text, chunk_size=700, overlap=120):
    words = text.split()
    chunks = []

    i = 0
    while i < len(words):
        chunk = words[i:i + chunk_size]

        if len(chunk) > 50:
            chunks.append(" ".join(chunk))

        i += chunk_size - overlap

    return chunks