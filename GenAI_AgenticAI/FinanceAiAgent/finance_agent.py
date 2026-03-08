from __future__ import annotations
from datetime import datetime
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

STOCKS = {
    "AAPL":     {"name":"Apple Inc.",          "price":189.30,  "change":+1.24,   "pe":29.1, "sector":"Technology",     "cur":"$"},
    "GOOGL":    {"name":"Alphabet Inc.",        "price":175.84,  "change":-0.67,   "pe":23.4, "sector":"Technology",     "cur":"$"},
    "MSFT":     {"name":"Microsoft Corp.",      "price":415.20,  "change":+2.10,   "pe":36.2, "sector":"Technology",     "cur":"$"},
    "TSLA":     {"name":"Tesla Inc.",           "price":248.50,  "change":-3.40,   "pe":62.1, "sector":"EV",             "cur":"$"},
    "NVDA":     {"name":"NVIDIA Corp.",         "price":875.40,  "change":+18.20,  "pe":68.3, "sector":"Semiconductors", "cur":"$"},
    "AMZN":     {"name":"Amazon.com",           "price":192.80,  "change":+0.95,   "pe":44.7, "sector":"Cloud/Commerce", "cur":"$"},
    "META":     {"name":"Meta Platforms",       "price":530.10,  "change":+4.30,   "pe":27.8, "sector":"Social Media",   "cur":"$"},
    "JPM":      {"name":"JPMorgan Chase",       "price":215.60,  "change":+1.80,   "pe":12.3, "sector":"Banking",        "cur":"$"},
    "RELIANCE": {"name":"Reliance Industries",  "price":2856.0,  "change":+34.5,   "pe":28.1, "sector":"Conglomerate",   "cur":"₹"},
    "TCS":      {"name":"Tata Consultancy",     "price":4120.0,  "change":-15.0,   "pe":31.2, "sector":"IT Services",    "cur":"₹"},
    "INFY":     {"name":"Infosys Ltd.",         "price":1845.0,  "change":+22.5,   "pe":26.4, "sector":"IT Services",    "cur":"₹"},
    "HDFC":     {"name":"HDFC Bank",            "price":1650.0,  "change":+8.75,   "pe":19.8, "sector":"Banking",        "cur":"₹"},
    "WIPRO":    {"name":"Wipro Ltd.",           "price":520.0,   "change":-5.50,   "pe":20.1, "sector":"IT Services",    "cur":"₹"},
    "HCLTECH":  {"name":"HCL Technologies",     "price":1720.0,  "change":+12.0,   "pe":24.5, "sector":"IT Services",    "cur":"₹"},
    "BTC":      {"name":"Bitcoin",              "price":67850.0, "change":+1250.0, "pe":None, "sector":"Crypto",         "cur":"$"},
    "ETH":      {"name":"Ethereum",             "price":3420.0,  "change":+85.0,   "pe":None, "sector":"Crypto",         "cur":"$"},
    "SPY":      {"name":"S&P 500 ETF",          "price":524.10,  "change":+3.20,   "pe":22.1, "sector":"ETF",            "cur":"$"},
    "NIFTYBEES":{"name":"Nifty BeES ETF",       "price":248.50,  "change":+1.80,   "pe":22.5, "sector":"ETF",            "cur":"₹"},
}
NEWS = {
    "NVDA":     ["NVIDIA reports record data center revenue $22.6B, beating estimates 8%","Jensen Huang announces Blackwell Ultra GPU at GTC 2025","NVDA added to Berkshire Hathaway portfolio"],
    "TCS":      ["TCS Q3 profit rises 5.4% YoY to ₹12,380 crore","TCS wins $1.5B UK government digital transformation deal","TCS hiring 40,000 freshers in FY2025"],
    "RELIANCE": ["Reliance Jio 5G coverage across all 1,000 Indian cities","RIL Q3 profit rises 11% to ₹18,540 crore","Reliance Retail targets 10,000 new stores by 2026"],
    "BTC":      ["Bitcoin ETFs see record $2.4B inflow in single day","MicroStrategy holds 400,000 BTC","El Salvador reports $40M profit on Bitcoin treasury"],
    "AAPL":     ["Apple Intelligence rolling out to 50+ countries Q2 2025","iPhone 17 pre-orders break records in India","Apple Services crosses $25B/quarter"],
    "default":  ["Markets rally on better-than-expected US CPI data (3.1%)","Fed signals two rate cuts in H2 2025","AI sector sees record $50B VC investment Q1 2025","India FII inflows turn positive ₹8,200 crore"],
}
CONCEPTS = {
    "pe ratio":       "Price-to-Earnings = Share Price ÷ Annual EPS. P/E of 25 means investors pay ₹25 per ₹1 profit. High P/E = growth expectations. Compare within same sector.",
    "sip":            "Systematic Investment Plan — fixed monthly investment in mutual funds. Benefits: rupee cost averaging, no timing stress, compounding over 10-20 years.",
    "nifty":          "NIFTY 50 tracks India's 50 largest companies by market cap on NSE. Primary benchmark for Indian equity market.",
    "sensex":         "SENSEX tracks top 30 companies on BSE. Along with NIFTY, the heartbeat of Indian stock market.",
    "diversification":"Spread across asset classes, sectors, geographies. If one sector falls, others cushion. Rule: no single stock >10% of portfolio.",
    "market cap":     "Share Price × Total Shares. India: Large-cap >₹20,000Cr, Mid-cap ₹5,000-20,000Cr, Small-cap <₹5,000Cr.",
    "roe":            "Return on Equity = Net Income ÷ Shareholder Equity. ROE >15% generally good, >25% exceptional.",
    "cagr":           "Compound Annual Growth Rate — steady annual rate needed to reach final value. CAGR 15% over 10 years: ₹1L becomes ₹4L.",
    "etf":            "Exchange-Traded Fund — basket of securities traded like a stock. Lower fees than mutual funds. NIFTY BeES tracks NIFTY 50.",
    "beta":           "Beta measures volatility vs market. Beta 1.5 = 50% more volatile than index. High beta = higher risk and reward.",
}

@tool
def get_stock_price(ticker: str) -> str:
    """Get price, daily change, P/E, sector for a ticker. US: AAPL,NVDA,TSLA,MSFT,GOOGL,META,AMZN,JPM. India: RELIANCE,TCS,INFY,HDFC,WIPRO,HCLTECH. Crypto: BTC,ETH. ETF: SPY,NIFTYBEES."""
    t = ticker.upper().strip()
    s = STOCKS.get(t) or next((v for k,v in STOCKS.items() if t in v["name"].upper()), None)
    if not s: return f"Ticker '{t}' not found. Available: {', '.join(STOCKS)}"
    pct = s["change"]/s["price"]*100; sign = "+" if pct>=0 else ""; arrow = "▲" if pct>=0 else "▼"
    pe = f"P/E: {s['pe']}" if s["pe"] else "P/E: N/A"
    return f"{s['name']} ({t})\nPrice: {s['cur']}{s['price']:,.2f}\n{arrow} {sign}{pct:.2f}% today\n{pe} | {s['sector']}\n[Simulated — {datetime.now().strftime('%d %b %Y')}]"

@tool
def analyze_portfolio(holdings: str) -> str:
    """Analyze portfolio allocation, sector breakdown, risk. Input: 'TICKER:QTY,TICKER:QTY' e.g. 'TCS:20,AAPL:5,BTC:0.5'"""
    try:
        portfolio = {t.strip().upper(): float(q.strip()) for part in holdings.split(",") if ":" in part for t,q in [part.split(":")] if t.strip().upper() in STOCKS}
        if not portfolio: return "Format: 'TCS:20,AAPL:5,BTC:0.5'"
        total = sum(STOCKS[t]["price"]*q for t,q in portfolio.items())
        allocs = {t: STOCKS[t]["price"]*q/total*100 for t,q in portfolio.items()}
        sectors: dict = {}
        for t in portfolio: sectors[STOCKS[t]["sector"]] = sectors.get(STOCKS[t]["sector"],0) + allocs[t]
        crypto = sum(v for t,v in allocs.items() if STOCKS[t]["sector"]=="Crypto")
        top = max(allocs.values()); risk = "HIGH 🔴" if (crypto>20 or top>50) else "MEDIUM 🟡" if top>30 else "LOW 🟢"
        lines = [f"Portfolio Analysis\nTotal: ${total:,.2f}\n\nTop Holdings:"]
        for t,p in sorted(allocs.items(),key=lambda x:-x[1])[:5]: lines.append(f"  {t}: {p:.1f}% ({STOCKS[t]['cur']}{STOCKS[t]['price']*portfolio[t]:,.2f})")
        lines.append(f"\nSectors:"); [lines.append(f"  {s}: {p:.1f}%") for s,p in sorted(sectors.items(),key=lambda x:-x[1])]
        lines.append(f"\nRisk: {risk}"); lines.append(f"Sectors: {len(sectors)} ({'✅ diversified' if len(sectors)>=4 else '⚠️ concentrate more'})")
        if top>40: lines.append(f"⚠️ {max(allocs,key=allocs.get)} is {top:.0f}% — rebalance recommended")
        return "\n".join(lines)
    except Exception as e: return f"Error: {e}. Use: 'TCS:20,AAPL:5,BTC:0.5'"

@tool
def get_market_news(ticker_or_topic: str) -> str:
    """Recent news for a ticker or topic. Examples: NVDA, TCS, BTC, market, AI stocks"""
    headlines = NEWS.get(ticker_or_topic.upper().strip(), NEWS["default"])
    return f"📰 {ticker_or_topic.upper()} News\n" + "\n".join(f"{i}. {h}" for i,h in enumerate(headlines,1)) + f"\n[{datetime.now().strftime('%d %b %Y')}]"

@tool
def explain_concept(concept: str) -> str:
    """Plain-English finance education. Knows: PE ratio, SIP, NIFTY, SENSEX, diversification, market cap, ROE, CAGR, ETF, beta."""
    cl = concept.lower().strip()
    for k,v in CONCEPTS.items():
        if k in cl or cl in k or any(w in cl for w in k.split()): return f"📚 {k.upper()}\n\n{v}"
    return f"I don't have '{concept}' stored but can explain it. Known: {', '.join(CONCEPTS)}"

@tool
def compare_stocks(tickers: str) -> str:
    """Side-by-side stock comparison. Input: comma-separated tickers e.g. 'TCS,INFY,WIPRO' or 'AAPL,MSFT,GOOGL'"""
    found = {t.strip().upper(): STOCKS[t.strip().upper()] for t in tickers.split(",") if t.strip().upper() in STOCKS}
    if not found: return f"No tickers found. Try: {', '.join(list(STOCKS)[:8])}"
    lines = ["Comparison","─"*56, f"{'Ticker':<10} {'Price':>13} {'Change%':>9} {'P/E':>8}  Sector","─"*56]
    for t,s in found.items():
        pct = s["change"]/s["price"]*100; sign = "+" if pct>=0 else ""; pe = str(s["pe"]) if s["pe"] else "N/A"
        lines.append(f"{t:<10} {s['cur']}{s['price']:>12,.2f} {sign}{pct:>8.2f}% {pe:>8}  {s['sector']}")
    if len(found)>1:
        pe_stocks = {t:s for t,s in found.items() if s["pe"]}
        if pe_stocks: lines.append(f"\n💡 Best value (lowest P/E): {min(pe_stocks,key=lambda t:pe_stocks[t]['pe'])}")
        lines.append(f"📈 Best today: {max(found,key=lambda t:found[t]['change']/found[t]['price'])}")
    return "\n".join(lines)

class State(TypedDict):
    messages: Annotated[list, add_messages]

SYSTEM = """You are a Finance AI Agent with market data tools.

Tools: get_stock_price, analyze_portfolio, get_market_news, explain_concept, compare_stocks

Supported tickers — US: AAPL,NVDA,TSLA,MSFT,GOOGL,META,AMZN,JPM | India: RELIANCE,TCS,INFY,HDFC,WIPRO,HCLTECH | Crypto: BTC,ETH | ETF: SPY,NIFTYBEES

Rules:
- ALWAYS call a tool before answering price/news/portfolio questions
- Use ₹ for Indian stocks, $ for US/Crypto
- Add disclaimer on investment recommendations: "⚠️ Educational — not financial advice"
- Under 220 words per response"""

def build_graph():
    tools = [get_stock_price, analyze_portfolio, get_market_news, explain_concept, compare_stocks]
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2).bind_tools(tools)
    tbn = {t.name:t for t in tools}

    def agent(state): return {"messages": [llm.invoke([SystemMessage(content=SYSTEM)]+state["messages"])]}
    def tool_node(state):
        last = state["messages"][-1]
        return {"messages": [ToolMessage(content=str(tbn[tc["name"]].invoke(tc["args"])),tool_call_id=tc["id"]) for tc in last.tool_calls if tc["name"] in tbn]}
    def route(state) -> Literal["tools","__end__"]: return "tools" if getattr(state["messages"][-1],"tool_calls",None) else END

    g = StateGraph(State)
    g.add_node("agent",agent); g.add_node("tools",tool_node)
    g.set_entry_point("agent")
    g.add_conditional_edges("agent",route,{"tools":"tools",END:END})
    g.add_edge("tools","agent")
    return g.compile()

graph = build_graph()

async def run_finance_agent(message: str, history: list[dict]) -> str:
    msgs = [HumanMessage(content=h["content"]) if h["role"]=="user" else AIMessage(content=h["content"]) for h in history]
    msgs.append(HumanMessage(content=message))
    result = await graph.ainvoke({"messages": msgs})
    return result["messages"][-1].content
