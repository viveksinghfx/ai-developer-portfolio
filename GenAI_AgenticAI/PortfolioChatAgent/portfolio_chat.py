from __future__ import annotations
from typing import Annotated, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

KB = {
    "projects": [
        {"name": "Finance AI Agent",       "tags": ["LangGraph","FastAPI","OpenAI"],         "highlights": ["5 tools","US+India+Crypto","<3s"]},
        {"name": "RAG Knowledge Base",     "tags": ["LangChain","Pinecone","AWS ECS"],        "highlights": ["10M+ docs","99.2% accuracy","<500ms"]},
        {"name": "Resume Screening Agent", "tags": ["LangGraph","OpenAI","S3","DynamoDB"],    "highlights": ["95% accuracy","5-10s","1000+ daily"]},
        {"name": "Real-Time AI Dashboard", "tags": ["Next.js","WebSockets","CloudWatch"],     "highlights": ["10k+ metrics/s","99.9% uptime"]},
    ],
    "skills": {
        "AI/ML": ["LangGraph","LangChain","RAG","Prompt Engineering","Multi-Agent Orchestration"],
        "Pipeline": ["Houdini/VEX","Procedural Systems","Python Automation","DAG Workflows","Unreal Blueprints"],
        "Languages": ["Python","TypeScript","VEX","SQL","Bash"],
        "Cloud": ["AWS Lambda","ECS Fargate","SageMaker","Docker","Kubernetes","Terraform"],
        "Data": ["Pinecone","DynamoDB","S3","Redis","PostgreSQL"],
    },
    "experience": [
        {"role": "Pipeline & AI Systems Engineer", "company": "Harikatha Studio",              "period": "Nov 2023 - Jan 2026"},
        {"role": "FX Pipeline Engineer",           "company": "Technicolor Animation",         "period": "Jul 2023 - Jun 2024"},
    ],
    "education": "MCA — Maharaja Agrasen Himalayan Garhwal University (2021-2023)",
    "contact": "hello@viveksingh.tech | linkedin.com/in/vivek-singh-633886137",
    "story": "3+ years building production Python pipelines and DAG-based procedural systems in Houdini & Unreal. Now applying the same graph-based thinking to LangGraph agents, RAG pipelines, and AWS-deployed AI systems. The mental model never changed — the domain did.",
}

@tool
def search_portfolio(query: str) -> str:
    """Search Vivek Singh's portfolio: projects, skills, experience, background, contact."""
    q = query.lower()
    results = []
    if any(w in q for w in ["project","built","work","rag","finance","resume","dashboard"]):
        for p in KB["projects"]:
            results.append(f"Project: {p['name']} | Tags: {', '.join(p['tags'])} | {', '.join(p['highlights'])}")
    if any(w in q for w in ["skill","tech","know","framework","cloud","language"]):
        for cat, skills in KB["skills"].items():
            results.append(f"{cat}: {', '.join(skills)}")
    if any(w in q for w in ["experience","job","work","company","background","story","pipeline","fx","houdini"]):
        for e in KB["experience"]:
            results.append(f"Experience: {e['role']} at {e['company']} ({e['period']})")
        results.append(f"Background: {KB['story']}")
    if any(w in q for w in ["contact","email","hire","reach","linkedin"]):
        results.append(f"Contact: {KB['contact']}")
    if any(w in q for w in ["education","degree","university","study"]):
        results.append(f"Education: {KB['education']}")
    if not results:
        results.append(f"Vivek Singh — Pipeline & AI Systems Engineer. Projects: {[p['name'] for p in KB['projects']]}. {KB['story']}")
    return "\n".join(results)

class State(TypedDict):
    messages: Annotated[list, add_messages]

SYSTEM = """You are an AI assistant for Vivek Singh's portfolio. Use the search_portfolio tool to look up accurate info.
Key fact: Vivek's background in Houdini DAG networks and Python pipeline automation directly maps to LangGraph architecture.
Be enthusiastic, professional, and concise (under 120 words)."""

def build_graph():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3).bind_tools([search_portfolio])
    def agent(state): return {"messages": [llm.invoke([SystemMessage(content=SYSTEM)] + state["messages"])]}
    def tools(state):
        last = state["messages"][-1]
        return {"messages": [ToolMessage(content=str(search_portfolio.invoke(tc["args"])), tool_call_id=tc["id"]) for tc in last.tool_calls]}
    def route(state): return "tools" if getattr(state["messages"][-1], "tool_calls", None) else END
    g = StateGraph(State)
    g.add_node("agent", agent); g.add_node("tools", tools)
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", route, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")
    return g.compile()

graph = build_graph()

async def run_portfolio_chat(message: str, history: list[dict]) -> str:
    msgs = [HumanMessage(content=h["content"]) if h["role"]=="user" else AIMessage(content=h["content"]) for h in history]
    msgs.append(HumanMessage(content=message))
    result = await graph.ainvoke({"messages": msgs})
    return result["messages"][-1].content
