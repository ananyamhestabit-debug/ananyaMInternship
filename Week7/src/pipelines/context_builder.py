import os
import json
from utils.file_loader import load_json  #loads chunks.json
from retriever.hybrid_retriever import HybridRetriever 
from retriever.reranker import Reranker
import re     #text splitting(sentence level)
from sentence_transformers import SentenceTransformer, util  #embedding+ cosine similarity

model = SentenceTransformer("all-MiniLM-L6-v2") #same model as query embedding == chunk embedding space


def get_relevant_snippet(query, text, model, top_n=2):  #top_n=2 : best 2 sentences nikalta
    sentences = re.split(r'(?<=[.!?])\s+', text)
    sentences = [s.strip() for s in sentences if len(s.strip()) > 30]  #s.strip: extra space hatata

    if len(sentences) == 0:
        return text[:300]  #fallback context if sentence split fails

    query_vec = model.encode(query, convert_to_tensor=True)
    sent_vecs = model.encode(sentences, convert_to_tensor=True)

    scores = util.cos_sim(query_vec, sent_vecs)[0].cpu().numpy()
    top_idx = scores.argsort()[::-1][:top_n]  #indices sort-> desecnding order me ->  top 2 

    selected = [sentences[i] for i in top_idx]  # best selected picked

    return " ".join(selected)  #combine


def build_context(system_chunks_file, query, top_k=5, user_chunks_file=None):  #top_k= final chunk count
    system_chunks = load_json(system_chunks_file)

    # merge user chunks if exist
    if user_chunks_file and os.path.exists(user_chunks_file):
        user_chunks = load_json(user_chunks_file)
        chunks = system_chunks + user_chunks
    else:
        chunks = system_chunks

    retriever = HybridRetriever(chunks)
    retrieved = retriever.retrieve(query, top_k=top_k * 3)  #oversampling: 5 chahiye: pehle 15 lao -> then reranker best chunega

    reranker = Reranker()
    reranked = reranker.rerank(query, retrieved)

    seen_ids = set()  #duplicates avoid 
    final_context = []

    for c in reranked:
        if c["chunk_id"] not in seen_ids:
            final_context.append(c)
            seen_ids.add(c["chunk_id"])

        if len(final_context) >= top_k:  #final limit ki kitne final aaenge chunks
            break

    return final_context