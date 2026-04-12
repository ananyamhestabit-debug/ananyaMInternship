from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")

def hallucination_score(answer, context):
    if isinstance(context, list):
        context = " ".join([c["content"] for c in context])

    if not answer or not context:
        return 0.0

    emb1 = model.encode(answer, convert_to_tensor=True)
    emb2 = model.encode(context, convert_to_tensor=True)

    score = util.cos_sim(emb1, emb2).item()
    return round(score, 2)


def confidence_score(answer, context):
    if isinstance(context, list):
        context = " ".join([c["content"] for c in context])

    if not answer:
        return 0.0

    emb1 = model.encode(answer, convert_to_tensor=True)
    emb2 = model.encode(context, convert_to_tensor=True)

    similarity = util.cos_sim(emb1, emb2).item()
    length_factor = min(len(answer) / 200, 1)

    score = 0.7 * similarity + 0.3 * length_factor
    return round(score, 2)