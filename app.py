import json
from datetime import date

import streamlit as st
from dotenv import load_dotenv

load_dotenv()

import llm  # noqa: E402
import memory  # noqa: E402

st.set_page_config(page_title="DealMemory", layout="wide")
st.title("DealMemory")
st.caption("A sales copilot that remembers every call, objection and promise.")

with open("data/seed_deals.json") as f:
    SEED = json.load(f)

SYSTEM = (
    "You are a sharp sales-enablement assistant. Be concrete and concise. "
    "If you are given memory context, ground every claim in it and cite dates. "
    "If you have no context, say what you would need to know."
)

# ---------- Sidebar ----------
with st.sidebar:
    use_memory = st.toggle("Memory ON (Hindsight)", value=True)
    account = st.selectbox("Account", list(SEED.keys()))

    st.divider()
    if st.button("Load demo history into memory"):
        items = SEED[account]
        bar = st.progress(0.0)
        for i, it in enumerate(items):
            memory.retain_interaction(account, it["type"], it["note"], it["date"])
            bar.progress((i + 1) / len(items))
        st.success(f"Retained {len(items)} interactions for {account}")

    st.divider()
    st.subheader("Log a new interaction")
    kind = st.selectbox("Type", ["Call", "Email", "Meeting", "Demo"])
    note = st.text_area("What happened?")
    if st.button("Save to memory") and note.strip():
        memory.retain_interaction(account, kind, note, date.today().isoformat())
        st.success("Retained.")

# ---------- Brief me ----------
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("Brief me for my next call", type="primary"):
        q = (
            f"Prepare me for my next call with {account}. Cover stakeholders, "
            "objections raised, competitors mentioned, promises or follow-ups "
            "still open, and the recommended approach."
        )
        with st.spinner("Thinking..."):
            if use_memory:
                st.session_state["brief"] = memory.reflect(q)
            else:
                st.session_state["brief"] = llm.ask(SYSTEM, q)
        st.session_state["brief_mode"] = "WITH memory" if use_memory else "WITHOUT memory"

if "brief" in st.session_state:
    st.subheader(f"Briefing ({st.session_state['brief_mode']})")
    st.write(st.session_state["brief"])

# ---------- Chat ----------
st.divider()
st.subheader("Ask about this deal")
if "messages" not in st.session_state:
    st.session_state.messages = []

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.write(m["content"])

if prompt := st.chat_input(f"Ask about {account}..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    context = ""
    if use_memory:
        memories = memory.recall(f"{account}: {prompt}")
        context = "\n".join(f"- {m}" for m in memories)

    user_msg = f"Account: {account}\n"
    if context:
        user_msg += f"Relevant memory:\n{context}\n\n"
    user_msg += f"Question: {prompt}"

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            reply = llm.ask(SYSTEM, user_msg)
        st.write(reply)
        if use_memory and context:
            with st.expander("Memories used (recall)"):
                st.text(context)
    st.session_state.messages.append({"role": "assistant", "content": reply})
