import streamlit as st
import requests
import os

API_URL = os.getenv("NEXUS_API_URL", "http://localhost:8000")

st.set_page_config(page_title="NEXUS AI", layout="centered")

st.markdown("""
<style>
body { background: #fff; color: #000; }
.stTextArea textarea { font-family: monospace; font-size: 13px; }
.stButton > button {
    background: #000;
    color: #fff;
    border-radius: 2px;
    border: none;
    padding: 0.5em 1.5em;
}
.stButton > button:hover { background: #333; }
pre { background: #f5f5f5; padding: 1em; font-size: 12px; overflow-x: auto; }
hr { border: 1px solid #000; }
</style>
""", unsafe_allow_html=True)

st.title("NEXUS AI")
st.caption("Autonomous Multi-Agent System — Day 5")
st.divider()

# --- CSV selector from data/ folder ---
st.subheader("CSV (optional — for analysis tasks)")

csv_files = []
try:
    resp = requests.get(f"{API_URL}/csv-files", timeout=5)
    if resp.status_code == 200:
        csv_files = resp.json().get("files", [])
except Exception:
    pass

csv_options = ["None (no CSV)"] + csv_files
csv_choice = st.selectbox("Select a CSV from the data/ folder:", csv_options)
csv_filename = None if csv_choice == "None (no CSV)" else csv_choice

if csv_filename:
    st.caption(f"Using: data/{csv_filename}")

st.divider()

# --- Task Input ---
st.subheader("Task")

example_tasks = [
    "Plan a startup in AI for healthcare",
    "Write a Python FastAPI REST API with CRUD endpoints for a todo app",
    "Analyze the CSV sales dataset and create a business strategy",
    "Design a RAG pipeline for 50k documents",
    "Generate backend architecture for a scalable web app",
]

selected = st.selectbox("Example tasks (or type your own below):", [""] + example_tasks)
task = st.text_area("Task", value=selected, height=80, label_visibility="collapsed")

run_btn = st.button("Run NEXUS AI")

st.divider()

# --- Output ---
if run_btn:
    if not task.strip():
        st.warning("Enter a task first.")
        st.stop()

    with st.spinner("Running pipeline... "):
        try:
            resp = requests.post(
                f"{API_URL}/run",
                json={"task": task, "csv_filename": csv_filename},
                timeout=600,
            )
        except requests.exceptions.ConnectionError:
            st.error("Cannot connect to API. Make sure backend is running: python -m uvicorn api:app --reload --port 8000")
            st.stop()

    if resp.status_code != 200:
        st.error(f"API error {resp.status_code}: {resp.text}")
        st.stop()

    data = resp.json()

    st.subheader("Flow")
    st.code(data.get("flow", ""), language="text")

    st.subheader("Result")
    st.markdown(data.get("report", ""))

    validator = data.get("validator", {})
    score = validator.get("score", data.get("score", "?"))
    status = validator.get("status", "PASS")
    st.markdown(f"**Status:** {status} &nbsp; **Score:** {score}/10 &nbsp; **Time:** {data.get('elapsed', '?')}s")

    if data.get("py_file"):
        st.info(f"Code saved: `{data['py_file']}`")
    if data.get("md_file"):
        st.info(f"Report saved: `{data['md_file']}`")
    if data.get("log_path"):
        st.caption(f"Log: {data['log_path']}")

    with st.expander("Agent logs"):
        st.text("\n".join(data.get("logs", [])))

st.divider()

# --- Memory panel ---
if st.button("Show Memory"):
    resp = requests.get(f"{API_URL}/memory")
    if resp.status_code == 200:
        mem = resp.json()
        st.subheader("Past Runs")
        for r in mem.get("past_runs", []):
            st.markdown(f"- **{r['task'][:60]}** — score: {r['score']}")
        st.subheader("Stored Facts")
        for f in mem.get("facts", []):
            st.markdown(f"- {f}")
    else:
        st.error("Memory fetch failed.")
