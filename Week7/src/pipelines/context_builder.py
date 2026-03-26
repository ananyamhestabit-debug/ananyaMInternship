def build_context(docs, k=5, filters=None):
    """
    Apply filters + return top-k results
    """

    #filters
    if filters:
        filtered_docs = []
        for doc in docs:
            match = True

            for key, value in filters.items():
                if doc["metadata"].get(key) != value:
                    match = False
                    break

            if match:
                filtered_docs.append(doc)
    else:
        filtered_docs = docs

    #returns top-k
    return filtered_docs[:k]