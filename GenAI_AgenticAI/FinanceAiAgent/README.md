# 💹 Finance AI Agent

An agentic finance assistant built with **LangGraph** and **GPT-4o-mini** that answers real-time stock queries, analyzes portfolios, fetches market news, and explains financial concepts — for both **US and Indian markets**.

---

## 🚀 Features

- **Stock Prices** — US (AAPL, NVDA, TSLA...), India (TCS, RELIANCE, INFY...), Crypto (BTC, ETH), ETFs
- **Portfolio Analyzer** — Allocation breakdown, sector diversification, risk scoring
- **Market News** — Simulated latest headlines per ticker
- **Concept Explainer** — P/E ratio, SIP, NIFTY, CAGR, Beta, ROE and more
- **Stock Comparator** — Side-by-side table with value/momentum picks
- **Multi-turn conversation** — Maintains context across messages

---

## 🏗️ Architecture

```
User Message
     │
     ▼
 LangGraph Agent (GPT-4o-mini)
     │
     ├── get_stock_price
     ├── analyze_portfolio
     ├── get_market_news
     ├── explain_concept
     └── compare_stocks
     │
     ▼
 Final Response
```

The agent uses **conditional edges** to loop through tool calls until no more tools are needed, then returns the final answer.

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Agent Framework | LangGraph |
| LLM | OpenAI GPT-4o-mini |
| Tools | Custom Python tools |
| Language | Python 3.10+ |

---

## ⚙️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/viveksinghfx/finance-ai-agent
cd finance-ai-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run
python finance_agent.py
```

---

## 💬 Example Queries

```
"What is the price of NVDA?"
"Compare TCS, INFY, and WIPRO"
"Analyze my portfolio: TCS:20, AAPL:5, BTC:0.5"
"Explain what a P/E ratio is"
"Show me latest news for BTC"
```

---

## 📁 File Structure

```
finance-ai-agent/
├── finance_agent.py     # Main agent + all tools + LangGraph graph
├── requirements.txt
├── .env.example
└── README.md
```

---

## ⚠️ Disclaimer

This project is for **educational purposes only**. All stock data is simulated and does not constitute financial advice.
