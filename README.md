# AI Research Agent (CrewAI + Groq + DuckDuckGo)

A single-agent research assistant built with CrewAI. Give it a topic, it
searches the web for free using DuckDuckGo, and writes a structured
Markdown report using Groq's `openai/gpt-oss-120b` model.

## File structure

```
ai-research-agent/
├── app.py
├── agent.py
├── tools/
│   ├── __init__.py
│   └── search_tool.py
├── requirements.txt
├── runtime.txt
├── .gitignore
├── .env.example
└── README.md
```

## Local setup

```bash
git clone https://github.com/<your-username>/ai-research-agent.git
cd ai-research-agent
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Paste your free Groq API key (from https://console.groq.com/keys) into
the sidebar when the app opens.

## Deploying to Streamlit Community Cloud

1. Push this repo to GitHub.
2. Go to https://share.streamlit.io and click "New app".
3. Select your repo, branch, and `app.py` as the entry point.
4. Under **Advanced settings → Secrets**, you can optionally pre-fill a
   default key so you don't have to paste it every time:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
   (This app currently reads the key from the sidebar input, not
   `st.secrets`, so this step is optional — it's just handy if you want
   a default value later.)
5. Click Deploy.

## Notes
- `ddgs` (formerly `duckduckgo-search`) is free and needs no API key,
  but can occasionally rate-limit if you run many searches quickly.
- `crewai[litellm]` is required because Groq model strings (`groq/...`)
  are routed through LiteLLM under the hood.
