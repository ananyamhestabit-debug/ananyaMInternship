import streamlit as st
import os
import time
import json

from memory.memory_store import MemoryStore
from pipelines.rag_pipeline import generate_answer
from pipelines.sql_pipeline import run_sql_pipeline
from pipelines.image_pipeline import image_query_text, image_query_image, extract_image_text
from evaluation.rag_eval import evaluate_answer
from utils.logger import log
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Knowledge Assistant", layout="wide")

# temp folders
TEMP_IMG_DIR = "data/temp/images"
TEMP_PDF_DIR = "data/temp/pdfs"

os.makedirs(TEMP_IMG_DIR, exist_ok=True)
os.makedirs(TEMP_PDF_DIR, exist_ok=True)

# memory init
if "memory" not in st.session_state:
    st.session_state.memory = MemoryStore()

memory = st.session_state.memory

# sidebar
st.sidebar.title("Recent Chats")

for m in memory.get_all():
    st.sidebar.write("Type:", m.get("type", ""))
    st.sidebar.write("Q:", m["q"])
    st.sidebar.divider()

# main UI
st.title("AI Knowledge Assistant")
st.write("Ask questions from documents, images, and data")

tab1, tab2, tab3 = st.tabs(["RAG", "SQL", "IMAGE"])


# RAG
with tab1:

    st.subheader("RAG Mode")

    mode = st.radio(
        "Choose mode",
        ["System Knowledge", "User PDF"]
    )

    q = st.text_input("Ask question")

    top_k = st.slider("Top-K chunks", 1, 5, 3)

    col1, col2 = st.columns(2)
    ask_btn = col1.button("Ask")
    clear_btn = col2.button("Clear Memory")

    if clear_btn:
        memory.clear()
        st.success("Memory cleared")

    #  SYSTEM MODE 
    if mode == "System Knowledge":

        if ask_btn and q:
            context_mem = memory.get()

            ans, context_used = generate_answer(
                q,
                context_mem,
                chunks_file="data/chunks/chunks.json"
            )

            context_used = context_used[:top_k]

            eval_result = evaluate_answer(ans, context_used)

            memory.add(q, ans)
            memory.buffer[-1]["type"] = "RAG-SYSTEM"

            st.session_state.ans = ans
            st.session_state.context_used = context_used
            st.session_state.eval = eval_result

    # USER PDF MODE
    elif mode == "User PDF":

        uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

        custom_chunks_file = None

        if uploaded_file:
            pdf_path = f"data/temp/pdfs/{uploaded_file.name}"

            with open(pdf_path, "wb") as f:
                f.write(uploaded_file.read())

            from PyPDF2 import PdfReader
            reader = PdfReader(pdf_path)

            text = ""
            for page in reader.pages:
                if page.extract_text():
                    text += page.extract_text() + "\n"

            from pipelines.ingest import chunk_text
            chunks = chunk_text(text, 700, 50)

            temp_chunks = []
            for i, c in enumerate(chunks):
                temp_chunks.append({
                    "chunk_id": f"user_{i}",
                    "content": c["content"],
                    "metadata": {"source": uploaded_file.name}
                })

            import json
            custom_chunks_file = f"data/chunks/user_{uploaded_file.name}.json"

            with open(custom_chunks_file, "w") as f:
                json.dump(temp_chunks, f)

            st.success("PDF ready")

        if ask_btn and q and custom_chunks_file:

            from pipelines.user_rag_pipeline import generate_user_answer

            context_mem = memory.get()

            ans, context_used = generate_user_answer(
                q,
                context_mem,
                custom_chunks_file
            )

            context_used = context_used[:top_k]

            eval_result = evaluate_answer(ans, context_used)

            memory.add(q, ans)
            memory.buffer[-1]["type"] = "RAG-USER"

            st.session_state.ans = ans
            st.session_state.context_used = context_used
            st.session_state.eval = eval_result

    # DISPLAY 
    if "ans" in st.session_state:
        st.subheader("Answer")
        st.write(st.session_state.ans)

        st.subheader("Evaluation")
        st.write("Hallucinated:", st.session_state.eval["hallucinated"])
        st.write("Confidence:", st.session_state.eval["confidence"])

        st.subheader("Context Used")
        for c in st.session_state.context_used:
            st.write(c["content"][:300])
            st.write("Source:", c["metadata"].get("source"))
            st.divider()

# SQL
with tab2:

    q = st.text_input("Ask SQL question")

    if st.button("Run Query") and q:
        result = run_sql_pipeline(q)

        if "error" in result:
            st.error(result["error"])
        else:
            st.code(result["sql"])
            st.table(result["rows"])

            
            memory.buffer[-1]["type"] = "SQL"


# IMAGE
with tab3:

    mode = st.radio("Mode", [
        "1. Text -> Image",
        "2. Image -> Image",
        "3. Image -> Text"
    ])

    # text to image
    if mode == "1. Text -> Image":
        q = st.text_input("Enter query")

        if st.button("Search"):
            results = image_query_text(q)

            for r in results:
                st.image(r["image"])
                st.write("Caption:", r["caption"])
                st.write("OCR:", r["ocr"][:200])
                st.divider()

            if results:
                memory.add(q, results[0]["caption"])
                memory.buffer[-1]["type"] = "IMAGE"

    # image to image
    elif mode == "2. Image -> Image":
        file = st.file_uploader("Upload image", type=["png", "jpg", "jpeg"])

        if file:
            path = os.path.join(TEMP_IMG_DIR, f"{int(time.time())}_{file.name}")

            with open(path, "wb") as f:
                f.write(file.read())

            st.image(path, caption="Uploaded Image")

            if st.button("Find Similar Images"):
                results = image_query_image(path)

                for i, r in enumerate(results):
                    st.image(r["image"])
                    st.write(f"Rank: {i+1}")
                    st.write("Distance:", round(r["score"], 3))
                    st.write("Caption:", r["caption"])
                    st.write("OCR:", r["ocr"][:200])
                    st.divider()

                if results:
                    memory.add("User Image Query", results[0]["caption"])
                    memory.buffer[-1]["type"] = "IMAGE"

    # image to text
    elif mode == "3. Image -> Text":
        file = st.file_uploader("Upload image")

        if file:
            path = os.path.join(TEMP_IMG_DIR, f"{int(time.time())}_{file.name}")

            with open(path, "wb") as f:
                f.write(file.read())

            st.image(path)

            if st.button("Extract"):
                result = extract_image_text(path)

                st.write("Caption:", result["caption"])

                if result["ocr"]:
                    st.write("OCR:", result["ocr"])
                else:
                    st.write("OCR: No text detected")

                memory.add("Image OCR", result["caption"])
                memory.buffer[-1]["type"] = "IMAGE"