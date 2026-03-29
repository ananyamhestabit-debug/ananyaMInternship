def evaluate(response):

    score = 0

    if response["text"]:
        score += 1

    if response["images"]:
        score += 1

    if response["sql"]["results"]:
        score += 1

    confidence = score / 3

    return {
        "score": score,
        "confidence": confidence
    }