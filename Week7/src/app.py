import streamlit as st
from memory.memory_store import MemoryStore
from pipelines.rag_pipeline import generate_answer
from pipelines.sql_pipeline import run_sql_pipeline
from pipelines.image_pipeline import image_query_text, image_query_image
from evaluation.rag_eval import hallucination_score, confidence_score
from utils.logger import log
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Knowledge Assistant", layout="wide")

# ---------------- MEMORY INIT ----------------
if "memory" not in st.session_state:
    st.session_state.memory = MemoryStore()

memory = st.session_state.memory

# ---------------- SIDEBAR ----------------
st.sidebar.title("Recent Chats")

# show last 5 chats (ALL systems)
for m in memory.get_all():
    st.sidebar.write("Type:", m["type"])
    st.sidebar.write("Q:", m["q"])
   
    st.sidebar.divider()

# ---------------- MAIN ----------------
st.title("AI Knowledge Assistant")
st.write("Ask questions from documents, images, and data")

tab1, tab2, tab3 = st.tabs(["RAG", "SQL", "IMAGE"])

# ---------------- RAG ----------------
with tab1:

    q = st.text_input("Ask question")

    top_k = st.slider("Top-K chunks", 1, 5, 3)

    col1, col2 = st.columns(2)
    ask_btn = col1.button("Ask")
    clear_btn = col2.button("Clear Memory")

    if clear_btn:
        memory.clear()
        st.success("Memory cleared")

    if ask_btn and q:
        context_mem = memory.get()

        ans, context_used = generate_answer(q, context_mem)
        context_used = context_used[:top_k]

        hall = hallucination_score(ans, context_used)
        conf = confidence_score(ans, context_used)

        #  store in memory
        memory.add(q, ans)
        memory.buffer[-1]["type"] = "RAG"

        log({
            "type": "rag",
            "q": q,
            "a": ans
        })

        st.session_state.ans = ans
        st.session_state.context_used = context_used
        st.session_state.conf = conf
        st.session_state.hall = hall

    if "ans" in st.session_state:
        st.subheader("Answer")
        st.write(st.session_state.ans)

        st.subheader("Scores")
        st.write("Confidence:", st.session_state.conf)
        st.write("Hallucination:", st.session_state.hall)

        st.subheader("Context Used")
        for i, c in enumerate(st.session_state.context_used):
            st.write(f"{i+1}. {c['content']}")
            st.divider()

# ---------------- SQL ----------------
with tab2:

    q = st.text_input("Ask SQL question")

    if st.button("Run Query") and q:
        result = run_sql_pipeline(q)

        if "error" in result:
            st.error(result["error"])
        else:
            st.code(result["sql"])
            st.table(result["rows"])
            st.write(result["summary"])

            #  store memory
            memory.add(q, result["summary"])
            memory.buffer[-1]["type"] = "SQL"

# ---------------- IMAGE ----------------
with tab3:

    mode = st.radio("Mode", [
        "Text → Image",
        "Image → Image",
        "Image → Text"
    ])

    # TEXT → IMAGE
    if mode == "Text → Image":
        q = st.text_input("Enter query")

        if st.button("Search"):
            results = image_query_text(q)

            for r in results:
                st.image(r["image"])
                st.write("Caption:", r["caption"])
                st.write("OCR:", r["ocr"][:200])
                st.divider()

            #  store memory
            if results:
                memory.add(q, results[0]["caption"])
                memory.buffer[-1]["type"] = "IMAGE"

    # IMAGE → IMAGE
    elif mode == "Image → Image":
        file = st.file_uploader("Upload image")

        if file:
            path = f"temp_{file.name}"
            with open(path, "wb") as f:
                f.write(file.read())

            if st.button("Find Similar"):
                results = image_query_image(path)

                for r in results:
                    st.image(r["image"])
                    st.write("Caption:", r["caption"])
                    st.divider()

                if results:
                    memory.add("Image Query", results[0]["caption"])
                    memory.buffer[-1]["type"] = "IMAGE"

    # IMAGE → TEXT
    elif mode == "Image → Text":
        file = st.file_uploader("Upload image")

        if file:
            st.image(file)

            path = f"temp_{file.name}"
            with open(path, "wb") as f:
                f.write(file.read())

            if st.button("Extract"):
                results = image_query_image(path)

                top = results[0]

                st.write("Caption:", top["caption"])
                st.write("OCR:", top["ocr"])

                memory.add("Image OCR", top["caption"])
                memory.buffer[-1]["type"] = "IMAGE"