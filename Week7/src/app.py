import streamlit as st
from memory.memory_store import MemoryStore
from pipelines.rag_pipeline import generate_answer
from pipelines.sql_pipeline import run_sql_pipeline
from pipelines.image_pipeline import image_query_text, image_query_image
from evaluation.rag_eval import hallucination_score, confidence_score
from utils.logger import log
from dotenv import load_dotenv

load_dotenv(dotenv_path="../.env")

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="",
    layout="wide"
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("System Info")
st.sidebar.markdown("""
### Multimodal RAG System

✔ Text RAG  
✔ Image RAG  
✔ SQL QA  
✔ Memory Enabled  
""")

# ---------------- INIT MEMORY ----------------
if "memory" not in st.session_state:
    st.session_state.memory = MemoryStore()

memory = st.session_state.memory

# ---------------- TITLE ----------------
st.title("AI Knowledge Assistant")
st.markdown("Ask questions from documents, images, and structured data")

# ---------------- TABS ----------------
tab1, tab2, tab3 = st.tabs([
    "RAG:Document Assistant",
    "SQL-QA:Data Insights",
    "IMAGE:Visual Search"
])

# RAG 
with tab1:
    if "ans" not in st.session_state:
        st.session_state.ans = None
    if "context_used" not in st.session_state:
        st.session_state.context_used = None

    q = st.text_input("Ask anything from your documents:", key="rag")

    top_k = st.slider(
    "Select number of context chunks (Top-K)",
    min_value=1,
    max_value=5,
    value=3
)

    col1, col2 = st.columns([1,1])

    with col1:
        ask_btn = st.button("Ask", key="rag_btn")
    with col2:
        clear_btn = st.button("Clear Memory")

    if clear_btn:
        st.session_state.memory = MemoryStore()
        st.success("Memory cleared!")

    if ask_btn and q:
        with st.spinner("Searching & Thinking..."):
            context_mem = memory.get()

            ans, context_used = generate_answer(q, context_mem)
            # apply top-k manually
            context_used = context_used[:top_k]

            hall = hallucination_score(ans, context_used)
            conf = confidence_score(ans)

            memory.add(q, ans)

        log({
            "type": "rag",
            "q": q,
            "a": ans,
            "confidence": conf,
            "hallucination": hall
        })

        st.session_state.ans = ans
        st.session_state.context_used = context_used
        st.session_state.conf = conf
        st.session_state.hall = hall

    # DISPLAY
    if st.session_state.ans:
        st.markdown("## Answer")
        st.write(st.session_state.ans)

        st.markdown("### Scores")
        st.write(f"**Confidence:** {st.session_state.conf}")
        st.write(f"**Hallucination:** {st.session_state.hall}")

        st.markdown(f"### Top {top_k} Context Chunks")
        for i, c in enumerate(st.session_state.context_used[:top_k]):
            st.markdown(f"**Result {i+1}**")
            st.write(c["content"])
            st.divider()

# SQL
with tab2:
    q = st.text_input("Ask questions about your data:", key="sql")

    if st.button("Run Query", key="sql_btn") and q:
        with st.spinner("Generating SQL & fetching results..."):
            result = run_sql_pipeline(q)

        if "error" in result:
            st.error(result["error"])
        else:
            st.markdown("### Generated SQL")
            st.code(result["sql"], language="sql")

            st.markdown("### Results")
            st.table(result["rows"])

            st.markdown("### Summary")
            st.write(result["summary"])

# IMAGE 
with tab3:
    mode = st.radio("Mode", ["1. Text -> Image", "2. Image -> Image", "3. Image -> Text"])

    #  TEXT -> IMAGE
    if mode == "1. Text -> Image":
        q = st.text_input("Enter query", key="img_text")

        if st.button("Search Image", key="btn_text_img"):
            results = image_query_text(q)

            for r in results:
                st.image(r["image"])
                st.write("Caption:", r["caption"])
                st.write("OCR:", r["ocr"][:200])
                st.write("Score:", r["score"])
                st.divider()

    # -------- IMAGE → IMAGE --------
    elif mode == "2. Image -> Image":
        file = st.file_uploader("Upload Image", key="img_img")

        if file:
            path = f"temp_{file.name}"
            with open(path, "wb") as f:
                f.write(file.read())

            if st.button("Find Similar Images", key="btn_img_img"):
                results = image_query_image(path)

                for r in results:
                    st.image(r["image"])
                    st.write("Caption:", r["caption"])
                    st.write("Score:", r["score"])
                    st.divider()

    # -------- IMAGE → TEXT --------
    elif mode == "3. Image -> Text":
        file = st.file_uploader("Upload Image for OCR + Caption", key="img_text_mode")

        if file:
            st.image(file, caption="Uploaded Image")

            path = f"temp_{file.name}"
            with open(path, "wb") as f:
                f.write(file.read())

            if st.button("Extract Text & Caption", key="btn_img_text"):
                results = image_query_image(path)

                top = results[0]

                st.write("### Caption")
                st.write(top["caption"])

                st.write("### OCR Text")
                st.write(top["ocr"])

                st.write("### Score")
                st.write(top["score"])