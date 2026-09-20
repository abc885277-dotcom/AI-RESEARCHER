"""Streamlit front-end for the single-agent CrewAI research app."""

import streamlit as st
from agent import run_research

st.set_page_config(page_title="AI Research Agent", page_icon="🔎", layout="centered")

st.title("🔎 AI Research Agent")
st.caption("A single CrewAI agent that searches the web (DuckDuckGo) and writes a report, powered by Groq's `openai/gpt-oss-120b`.")

with st.sidebar:
    st.header("⚙️ Settings")
    groq_api_key = st.text_input(
        "Groq API Key",
        type="password",
        help="Get a free key at https://console.groq.com/keys — it is not stored anywhere, just used for this session.",
    )
    st.markdown("---")
    st.markdown(
        "**How it works:**\n"
        "1. Enter your topic\n"
        "2. The agent searches DuckDuckGo\n"
        "3. It writes a structured Markdown report using Groq"
    )

topic = st.text_input(
    "Enter a research topic",
    placeholder="e.g. Impact of AI on renewable energy in 2026",
)

run_button = st.button("Generate Report", type="primary")

if run_button:
    if not groq_api_key.strip():
        st.error("Please enter your Groq API key in the sidebar.")
    elif not topic.strip():
        st.error("Please enter a research topic.")
    else:
        with st.spinner("Researching... this can take a minute or two."):
            try:
                report = run_research(topic.strip(), groq_api_key.strip())
                st.session_state["report"] = report
            except Exception as e:
                st.error(f"Something went wrong: {e}")

if "report" in st.session_state:
    st.markdown("---")
    st.subheader("📄 Report")
    st.markdown(st.session_state["report"])
    st.download_button(
        "⬇️ Download report as Markdown",
        data=st.session_state["report"],
        file_name="research_report.md",
        mime="text/markdown",
    )
