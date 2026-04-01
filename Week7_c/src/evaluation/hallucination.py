def detect_hallucination(query, response):

    #  remove useless words
    stopwords = {"show", "what", "is", "the", "all", "give", "list", "me", "explain"}

    query_words = set(query.lower().split()) - stopwords

    if len(query_words) == 0:
        return True

    #  combine all text + captions
    text_data = " ".join([item["text"] for item in response["text"]]).lower()
    image_data = " ".join([item["caption"] for item in response["images"]]).lower()

    combined_data = text_data + " " + image_data

    # count meaningful matches
    match_count = sum(1 for word in query_words if word in combined_data)

    # LOGIC:
    # if only 1 weak match → still hallucination
    if match_count < 2:
        return True

    return False