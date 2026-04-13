from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")


def evaluate_answer(answer, context):
    if isinstance(context, list):
        context_text = " ".join([c["content"] for c in context])
    else:
        context_text = context

    if not answer or not context_text:
        return {
            "hallucinated": True,
            "confidence": 0.0,
            "faithfulness": "low"
        }

    emb1 = model.encode(answer, convert_to_tensor=True)
    emb2 = model.encode(context_text, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2).item()

    # -------- hallucination logic --------
    hallucinated = similarity < 0.5

    # -------- confidence --------
    length_factor = min(len(answer) / 200, 1)
    confidence = round(0.7 * similarity + 0.3 * length_factor, 2)

    # -------- faithfulness label --------
    if similarity > 0.7:
        faithfulness = "high"
    elif similarity > 0.5:
        faithfulness = "medium"
    else:
        faithfulness = "low"

    return {
        "hallucinated": hallucinated,
        "confidence": confidence,
        "faithfulness": faithfulness,
        "similarity": round(similarity, 2)
    }