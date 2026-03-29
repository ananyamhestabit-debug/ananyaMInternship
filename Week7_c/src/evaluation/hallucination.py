def detect_hallucination(query, response):

    # CASE 1: completely empty
    if not response["text"] and not response["images"] and not response["sql"]["results"]:
        return True

    #  remove useless words
    stopwords = {"show", "what", "is", "the", "all", "give", "list", "me"}

    query_words = set(query.lower().split()) - stopwords

    #  if no meaningful words left
    if len(query_words) == 0:
        return True

    #  combine all text
    text_data = " ".join([item["text"] for item in response["text"]]).lower()

    #  count meaningful matches
    match_count = sum(1 for word in query_words if word in text_data)

    # STRICT CONDITION
    if match_count == 0:
        return True

    return False