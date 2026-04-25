from sentence_transformers import CrossEncoder

#brings best relevant chunks according to the query at top(reorders the result in best order)
class Reranker:
    def __init__(self, model_name="cross-encoder/ms-marco-MiniLM-L-6-v2"):
        self.model = CrossEncoder(model_name) #query + text pair model : accurate hota as full attention

    def rerank(self, query, chunks):
        texts = [c["content"] for c in chunks]
        scores = self.model.predict([[query, t] for t in texts])  #score of each chunk
        for i, c in enumerate(chunks):
            c["score"] = float(scores[i])
        
        chunks.sort(key=lambda x: x["score"], reverse=True)  #highest score top
        return chunks