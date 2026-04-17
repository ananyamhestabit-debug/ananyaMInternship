from sentence_transformers import SentenceTransformer, util

model = SentenceTransformer("all-MiniLM-L6-v2")  #context embedding == answer embedding space

#checks hallucination(answer matches contect or not) and confidence
def evaluate_answer(answer, context):  #llm ka answer and context(retieved chunks)
    if isinstance(context, list):  #if contetx is chunks list  then combine and use a ssingle text
        context_text = " ".join([c["content"] for c in context])
    else:  #already string toh direct use
        context_text = context

    if not answer or not context_text:  #if anything is missing
        return {
            "hallucinated": True,
            "confidence": 0.0,
            "faithfulness": "low"
        }

    emb1 = model.encode(answer, convert_to_tensor=True)  #ans->vector
    emb2 = model.encode(context_text, convert_to_tensor=True) #contetx->vector

    similarity = util.cos_sim(emb1, emb2).item()  #cosine similarity

    #  hallucination logic 
    hallucinated = similarity < 0.5  #boundary between relevant vs hallucinated

    #  confidence
    length_factor = min(len(answer) / 200, 1)  #ans length score 
    confidence = round(0.7 * similarity + 0.3 * length_factor, 2)  #meaning>length

    # faithfulness label 
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