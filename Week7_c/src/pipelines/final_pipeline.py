from src.retriever.hybrid_retriever import advanced_search
from src.retriever.multimodal_search import text_to_image_search
from src.pipelines.sql_pipeline import run_sql_query
from src.memory.memory_store import add_to_memory
from src.logs.logger import log_chat
from src.evaluation.rag_eval import evaluate
from src.evaluation.hallucination import detect_hallucination


def filter_text_results(query, results):
    query_words = set(query.lower().split())

    stopwords = {"show", "what", "is", "the", "all", "give", "list", "me", "explain"}
    query_words = query_words - stopwords

    filtered = []

    for item in results:
        text = item["text"].lower()

        match_count = sum(1 for word in query_words if word in text)

        # BALANCED CONDITION
        if match_count >= 1:
            filtered.append(item)

    return filtered


def filter_image_results(query, results):
    query_words = set(query.lower().split())

    stopwords = {"show", "what", "is", "the", "all", "give", "list", "me", "explain"}
    query_words = query_words - stopwords

    filtered = []

    for item in results:
        caption = item["caption"].lower()

        match_count = sum(1 for word in query_words if word in caption)

        if match_count >= 1:
            filtered.append(item)

    return filtered


def final_system(query):

    # 🔹 TEXT RAG
    text_results = advanced_search(query, 3)
    text_results = filter_text_results(query, text_results)

    # 🔹 IMAGE RAG
    image_results = text_to_image_search(query, 2)
    image_results = filter_image_results(query, image_results)

    # 🔹 SQL QA
    sql_results = run_sql_query(query)

    # 🔹 BUILD RESPONSE
    response = {
        "text": text_results,
        "images": image_results,
        "sql": sql_results
    }

    # 🔹 MEMORY
    add_to_memory(query, response)

    # 🔹 LOGGING
    log_chat(query, response)

    # 🔹 EVALUATION
    eval_result = evaluate(response)

    # 🔹 HALLUCINATION
    hallucination = detect_hallucination(query, response)

    return {
        "response": response,
        "evaluation": eval_result,
        "hallucination": hallucination
    }