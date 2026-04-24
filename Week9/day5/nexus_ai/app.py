import streamlit as st
import sys
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)

st.set_page_config(
    page_title="NEXUS AI",
    page_icon="⬡",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@300;600;800&display=swap');

:root {
    --neon: #00ffe7;
    --neon2: #ff2d78;
    --dark: #070b14;
    --card: #0d1526;
    --border: #1a2a44;
    --text: #c8d8f0;
    --dim: #4a6080;
}

html, body, [data-testid="stAppViewContainer"] {
    background: var(--dark) !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
}
[data-testid="stSidebar"] {
    background: #080e1c !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebarContent"] {
    padding: 1rem 0.8rem !important;
}
header[data-testid="stHeader"] { display: none; }
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }

.nexus-title {
    font-family: 'Exo 2', sans-serif;
    font-weight: 800;
    font-size: 2.2rem;
    letter-spacing: 0.15em;
    color: var(--neon);
    text-shadow: 0 0 30px rgba(0,255,231,0.3);
    margin: 0;
}
.nexus-sub {
    font-size: 0.7rem;
    color: var(--dim);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 3px;
}
.nexus-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 16px;
    margin-bottom: 20px;
}
.msg-user {
    background: #111d33;
    border-left: 3px solid var(--neon2);
    border-radius: 0 8px 8px 0;
    padding: 12px 16px;
    margin: 8px 0;
    font-size: 0.9rem;
}
.msg-nexus {
    background: var(--card);
    border-left: 3px solid var(--neon);
    border-radius: 0 8px 8px 0;
    padding: 14px 18px;
    margin: 8px 0;
    font-size: 0.9rem;
    line-height: 1.7;
}
.msg-label {
    font-size: 0.62rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-bottom: 6px;
    font-family: 'Exo 2', sans-serif;
    font-weight: 600;
}
.label-user { color: var(--neon2); }
.label-nexus { color: var(--neon); }
.pipeline-wrap {
    display: flex;
    align-items: center;
    gap: 5px;
    flex-wrap: wrap;
    margin-bottom: 8px;
}
.pipe-badge {
    background: #0a1628;
    border: 1px solid var(--border);
    color: var(--neon);
    font-size: 0.62rem;
    font-family: 'Exo 2', sans-serif;
    font-weight: 600;
    letter-spacing: 0.1em;
    padding: 2px 9px;
    border-radius: 2px;
    text-transform: uppercase;
}
.pipe-arrow { color: var(--dim); font-size: 0.75rem; }
.mem-tag {
    background: #0a1a12;
    border: 1px solid #1a4030;
    color: #40e080;
    font-size: 0.62rem;
    padding: 2px 8px;
    border-radius: 2px;
    display: inline-block;
    margin: 2px 3px;
}
.mem-header {
    font-size: 0.62rem;
    color: #40e080;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-family: 'Exo 2', sans-serif;
}
.stat-card {
    background: #0a1220;
    border: 1px solid var(--border);
    border-radius: 5px;
    padding: 8px 12px;
    margin: 5px 0;
}
.stat-label { font-size: 0.6rem; color: var(--dim); letter-spacing: 0.18em; text-transform: uppercase; }
.stat-value { font-size: 1.25rem; color: var(--neon); font-family: 'Exo 2', sans-serif; font-weight: 800; }
.sec-lbl {
    font-size: 0.6rem; color: var(--dim);
    letter-spacing: 0.2em; text-transform: uppercase;
    margin: 10px 0 5px 0;
}
.agent-row { font-size: 0.72rem; color: #2a4060; padding: 2px 0; }
.mem-row   { font-size: 0.72rem; color: #2a5040; padding: 2px 0; }
.step-box {
    background: #090f1e;
    border: 1px solid var(--border);
    border-radius: 4px;
    padding: 10px 14px;
    margin: 4px 0;
    font-size: 0.78rem;
    color: #8aa0c0;
    white-space: pre-wrap;
    max-height: 200px;
    overflow-y: auto;
}
.step-title {
    font-size: 0.6rem;
    color: var(--dim);
    letter-spacing: 0.2em;
    text-transform: uppercase;
    margin-bottom: 4px;
    font-family: 'Exo 2', sans-serif;
}
.mem-badge-mode {
    font-size: 0.6rem;
    background: #0a1628;
    border: 1px solid var(--border);
    color: var(--dim);
    padding: 2px 8px;
    border-radius: 2px;
    display: inline-block;
    margin-bottom: 6px;
}
[data-testid="stChatInput"] textarea {
    background: #0a1220 !important;
    border: 1px solid var(--border) !important;
    color: var(--text) !important;
    font-family: 'Share Tech Mono', monospace !important;
    border-radius: 4px !important;
}
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--dark); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.stButton > button {
    background: transparent !important;
    border: 1px solid var(--border) !important;
    color: var(--dim) !important;
    font-family: 'Share Tech Mono', monospace !important;
    font-size: 0.72rem !important;
    border-radius: 3px !important;
}
.stButton > button:hover {
    border-color: var(--neon) !important;
    color: var(--neon) !important;
}
</style>
""", unsafe_allow_html=True)

# ── SESSION STATE DEFAULTS (must happen before any widget) ─────────────────────
if "messages"      not in st.session_state: st.session_state.messages      = []
if "total_queries" not in st.session_state: st.session_state.total_queries = 0
if "mem_count"     not in st.session_state: st.session_state.mem_count     = 0
if "vec_mode"      not in st.session_state: st.session_state.vec_mode      = "loading"
if "system"        not in st.session_state: st.session_state.system        = None
if "init_error"    not in st.session_state: st.session_state.init_error    = None

# ── LAZY INIT (only once) ──────────────────────────────────────────────────────
if st.session_state.system is None and st.session_state.init_error is None:
    try:
        from orchestrator.nexus import NexusAI
        st.session_state.system   = NexusAI()
        st.session_state.vec_mode = st.session_state.system.vector_store.mode
        st.session_state.mem_count = len(st.session_state.system.long_term_memory.retrieve_all())
    except Exception as e:
        st.session_state.init_error = str(e)

# ── SIDEBAR ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='margin-bottom:18px;'>
        <div style='font-family:"Exo 2",sans-serif;font-weight:800;font-size:1.2rem;
                    color:#00ffe7;letter-spacing:.14em;
                    text-shadow:0 0 18px rgba(0,255,231,0.25);'>
            ⬡ NEXUS AI
        </div>
        <div style='font-size:0.58rem;color:#2a4060;letter-spacing:.25em;
                    text-transform:uppercase;margin-top:2px;'>
            Autonomous Multi-Agent System
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Stats
    st.markdown(f"""
    <div class='stat-card'>
        <div class='stat-label'>Queries Processed</div>
        <div class='stat-value'>{st.session_state.total_queries:03d}</div>
    </div>
    <div class='stat-card'>
        <div class='stat-label'>Memory Entries</div>
        <div class='stat-value'>{st.session_state.mem_count:03d}</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # Active agents
    st.markdown("<div class='sec-lbl'>Active Agents</div>", unsafe_allow_html=True)
    for a in ["Researcher", "Coder", "Optimizer", "Reporter", "Personal"]:
        st.markdown(f"<div class='agent-row'>▸ {a}</div>", unsafe_allow_html=True)

    st.markdown("---")

    # Memory systems
    st.markdown("<div class='sec-lbl'>Memory Systems</div>", unsafe_allow_html=True)
    st.markdown("<div class='mem-row'>◈ Session (RAM)</div>", unsafe_allow_html=True)
    st.markdown("<div class='mem-row'>◈ Long-Term (SQLite)</div>", unsafe_allow_html=True)

    vec_label = st.session_state.vec_mode
    vec_color = "#40e080" if vec_label == "faiss" else "#888"
    st.markdown(
        f"<div style='font-size:.72rem;color:{vec_color};padding:2px 0;'>"
        f"◈ Vector ({'FAISS' if vec_label == 'faiss' else 'Keyword fallback'})</div>",
        unsafe_allow_html=True
    )

    st.markdown("---")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.markdown(
        "<div style='font-size:0.58rem;color:#1a2a44;margin-top:16px;'>"
        "Week 9 · Day 5 · NEXUS AI</div>",
        unsafe_allow_html=True
    )

# ── MAIN AREA ──────────────────────────────────────────────────────────────────
st.markdown("""
<div class='nexus-header'>
    <div class='nexus-title'>⬡ NEXUS AI</div>
    <div class='nexus-sub'>Multi-Agent Orchestration · Memory · Tools · Planning</div>
</div>
""", unsafe_allow_html=True)

# Init error banner
if st.session_state.init_error:
    st.error(f"System init failed: {st.session_state.init_error}")
    st.info("Check that your `.env` file has `OPENAI_API_KEY` and `MODEL_NAME` set correctly.")
    st.stop()

# ── CHAT HISTORY ───────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(f"""
        <div class='msg-user'>
            <div class='msg-label label-user'>▸ You</div>
            {msg['content']}
        </div>
        """, unsafe_allow_html=True)
    else:
        data = msg.get("data", {})
        pipeline    = data.get("pipeline", [])
        memory_hits = data.get("memory_hits", [])
        steps       = data.get("steps", [])
        final       = data.get("final", msg["content"])


        # Memory hits
        if memory_hits:
            tags = "".join(
                f"<span class='mem-tag'>{h[:65]}{'...' if len(h)>65 else ''}</span>"
                for h in memory_hits[:3]
            )
            
        # Main response
        safe_final = str(final).replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        st.markdown(f"""
        <div class='msg-nexus'>
            <div class='msg-label label-nexus'>◈ NEXUS</div>
            {safe_final}
        </div>
        """, unsafe_allow_html=True)

        # Step details
        if steps and len(steps) > 1:
            with st.expander("View agent steps", expanded=False):
                for step in steps:
                    preview = step["output"][:500] + "..." if len(step["output"]) > 500 else step["output"]
                    st.markdown(
                        f"<div class='step-title'>[ {step['agent'].upper()} ]</div>"
                        f"<div class='step-box'>{preview}</div>",
                        unsafe_allow_html=True
                    )

# ── CHAT INPUT ─────────────────────────────────────────────────────────────────
prompt = st.chat_input("Enter task or query...")

if prompt and st.session_state.system:
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.session_state.total_queries += 1

    with st.spinner("⬡ Processing pipeline..."):
        try:
            result = st.session_state.system.run(prompt)
            st.session_state.mem_count = len(
                st.session_state.system.long_term_memory.retrieve_all()
            )
            st.session_state.vec_mode = st.session_state.system.vector_store.mode
            final_text = result.get("final", "No response.")
            st.session_state.messages.append({
                "role": "assistant",
                "content": final_text,
                "data": result,
            })
        except Exception as e:
            st.session_state.messages.append({
                "role": "assistant",
                "content": f"Error: {str(e)}",
                "data": {},
            })

    st.rerun()
