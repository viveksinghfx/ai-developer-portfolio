# 🔬 Multi-Agent Research System

An autonomous research agent built with **LangGraph** that takes any topic, decomposes it into sub-questions, searches the web, and synthesizes a structured research report — all without human intervention.

---

## 🚀 Features

- **Query Decomposition** — Breaks complex topics into targeted sub-questions
- **Web Search** — Live search via DuckDuckGo (with fallback simulation)
- **Self-Correcting Loop** — Iterates up to 6 steps, routing between search and synthesis
- **Structured Reports** — Executive summary, key findings, challenges, and applications
- **Multi-turn memory** — Maintains conversation context

---

## 🏗️ Architecture

```
User Topic
     │
     ▼
 LangGraph Agent (GPT-4o-mini)
     │
     ├── decompose_query  ──→ Sub-questions + search queries
     │
     ├── web_search (x2-3) ──→ Live web results
     │
     └── Synthesize ──→ Structured Report
```

The agent uses a **step counter** to prevent infinite loops — automatically finalizes the report after 6 reasoning steps.

---

## 📄 Output Format

Every research report includes:

```
## Executive Summary
2-3 sentence overview

## Key Findings
- Finding 1
- Finding 2
...

## Challenges
## Applications
```

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Agent Framework | LangGraph |
| LLM | OpenAI GPT-4o-mini |
| Web Search | DuckDuckGo (langchain-community) |
| Language | Python 3.10+ |

---

## ⚙️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/viveksinghfx/multi-agent-research
cd multi-agent-research

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run
python research_agent.py
```

---

## 💬 Example Queries

```
"What is the current state of multimodal AI?"
"Explain recent advances in protein folding"
"Research the impact of AI on software engineering jobs"
"What are the latest developments in quantum computing?"
```

---

## 📁 File Structure

```
multi-agent-research/
├── research_agent.py    # Agent + tools + LangGraph graph
├── requirements.txt
├── .env.example
└── README.md
```
