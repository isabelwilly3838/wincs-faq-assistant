"""Streamlit chat UI.  Run:  streamlit run app.py"""
import csv
import datetime as dt
from pathlib import Path

import streamlit as st

from assistant.core import ask, load_kb

LOG = Path(__file__).parent / "logs" / "feedback.csv"

st.set_page_config(page_title="WinCS FAQ Assistant", page_icon="💬")
st.title("WinCS FAQ Assistant")
st.caption("Ask about membership, events, mentoring or volunteering. Answers come only from the WinCS FAQ.")


@st.cache_resource
def kb():
    return load_kb()


def log_feedback(question: str, answer: str, status: str, rating: str) -> None:
    LOG.parent.mkdir(exist_ok=True)
    new = not LOG.exists()
    with LOG.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["timestamp", "question", "answer", "status", "rating"])
        w.writerow([dt.datetime.now().isoformat(timespec="seconds"), question, answer, status, rating])


if "messages" not in st.session_state:
    st.session_state.messages = []  # each: role, content, status, sources, question

with st.sidebar:
    st.subheader("Try asking")
    for example in ["How much does membership cost?", "When are weekly meetings?", "How do I get a mentor?"]:
        if st.button(example, use_container_width=True):
            st.session_state.pending = example
    if st.button("Clear chat", type="secondary"):
        st.session_state.messages = []
        st.rerun()

for i, m in enumerate(st.session_state.messages):
    with st.chat_message(m["role"]):
        st.markdown(m["content"])
        if m["role"] == "assistant":
            if m.get("sources"):
                with st.expander("Sources"):
                    for s in m["sources"]:
                        st.write("•", s)
            c1, c2, _ = st.columns([1, 1, 8])
            if c1.button("👍", key=f"up{i}"):
                log_feedback(m["question"], m["content"], m["status"], "up")
                st.toast("Thanks for the feedback!")
            if c2.button("👎", key=f"down{i}"):
                log_feedback(m["question"], m["content"], m["status"], "down")
                st.toast("Thanks, we'll use this to improve.")

question = st.chat_input("Type your question…") or st.session_state.pop("pending", None)
if question:
    history = [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
    st.session_state.messages.append({"role": "user", "content": question})
    with st.spinner("Looking that up…"):
        a = ask(question, history=history, chunks=kb())
    st.session_state.messages.append(
        {"role": "assistant", "content": a.text, "status": a.status, "sources": a.sources, "question": question}
    )
    st.rerun()
