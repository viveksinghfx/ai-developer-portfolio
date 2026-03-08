# 🤖 Portfolio Chat Agent

An AI-powered chatbot built with **LangGraph** that answers questions about Vivek Singh's portfolio — projects, skills, experience, and background. Uses a knowledge base tool with intelligent query routing.

---

## 🚀 Features

- **Project Search** — Retrieves details on all portfolio projects with tech stack and highlights
- **Skills Lookup** — AI/ML, Cloud, Data, Languages, Pipeline skills
- **Experience & Background** — Work history and the FX → AI career transition story
- **Contact Info** — Email and LinkedIn on request
- **Multi-turn conversation** — Maintains context across the session

---

## 🏗️ Architecture

```
User Question
      │
      ▼
 LangGraph Agent (GPT-4o-mini)
      │
      └── search_portfolio(query) ──→ KB lookup ──→ Answer
```

A simple **ReAct-style agent** with a single knowledge base tool. The agent decides when to call the tool based on the user's question.

---

## 📦 Knowledge Base

The built-in KB covers:

| Category | Content |
|----------|---------|
| Projects | Finance Agent, RAG KB, Resume Agent, AI Dashboard |
| Skills | AI/ML, Pipeline, Cloud, Data, Languages |
| Experience | Pipeline & AI Systems Engineer, FX Pipeline Engineer |
| Education | MCA — Maharaja Agrasen Himalayan Garhwal University |
| Story | The FX → AI career transition narrative |

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Agent Framework | LangGraph |
| LLM | OpenAI GPT-4o-mini |
| Knowledge Base | In-memory Python dict |
| Language | Python 3.10+ |

---

## ⚙️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/viveksinghfx/portfolio-chat-agent
cd portfolio-chat-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run
python portfolio_chat.py
```

---

## 💬 Example Queries

```
"What projects has Vivek built?"
"What cloud technologies does he know?"
"Tell me about his background"
"How did he transition from FX to AI?"
"How can I contact Vivek?"
```

---

## 📁 File Structure

```
portfolio-chat-agent/
├── portfolio_chat.py    # Agent + KB tool + LangGraph graph
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🔧 Customization

To adapt this for your own portfolio, edit the `KB` dictionary in `portfolio_chat.py` with your own projects, skills, and experience.
