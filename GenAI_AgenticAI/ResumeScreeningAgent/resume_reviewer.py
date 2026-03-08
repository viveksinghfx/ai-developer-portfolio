from __future__ import annotations
import re
import io
from typing import Annotated, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
import PyPDF2

AI_KEYWORDS = ["python","machine learning","llm","langchain","docker","kubernetes","aws","fastapi",
    "sql","postgresql","redis","git","mlops","rag","vector","transformer","nlp","pytorch","tensorflow"]
WEAK_VERBS = ["worked on","helped with","was responsible for","assisted","participated in"]

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """Extract plain text from PDF bytes."""
    try:
        reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        return text.strip()
    except Exception:
        return ""

@tool
def ats_scan(resume_text: str) -> str:
    """Scan resume for ATS keywords relevant to AI/ML roles."""
    low = resume_text.lower()
    found = [k for k in AI_KEYWORDS if k in low]
    missing = [k for k in AI_KEYWORDS if k not in low]
    score = int(len(found)/len(AI_KEYWORDS)*100)
    return f"ATS Score: {score}/100\nFound ({len(found)}): {', '.join(found[:12])}\nMissing high-value: {', '.join(missing[:8])}"

@tool
def impact_analysis(resume_text: str) -> str:
    """Analyse impact statements and action verbs in resume bullets."""
    lines = [l.strip() for l in resume_text.split("\n") if len(l.strip()) > 20]
    numbered = [l for l in lines if re.search(r"\d+[%x+]?|\$[\d,]+|[\d,]+\+?", l)]
    weak = [v for v in WEAK_VERBS if v in resume_text.lower()]
    pct = int(len(numbered)/max(len(lines),1)*100)
    return f"Quantified bullets: {len(numbered)}/{len(lines)} ({pct}%)\nWeak verbs found: {', '.join(weak) if weak else 'None — good!'}"

class State(TypedDict):
    messages: Annotated[list, add_messages]
    resume_text: str
    ats: str
    impact: str

SYSTEM = """You are an expert resume reviewer for AI/ML roles.
Format your review:
## Overall Score (X/10)
## ATS Analysis
## Impact Statements
## Top 3 Improvements (numbered, specific)
Be direct and actionable. Under 280 words."""

def build_graph():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.2)

    def node_extract(state):
        last = next((m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None)
        text = last.content if last else ""
        if len(text) < 50:
            text = ""
        return {"resume_text": text}

    def node_ats(state):
        if len(state["resume_text"]) < 50:
            return {"ats": "No resume text detected."}
        try:
            return {"ats": ats_scan.invoke({"resume_text": state["resume_text"]})}
        except Exception as e:
            return {"ats": f"ATS scan failed: {str(e)}"}

    def node_impact(state):
        if len(state["resume_text"]) < 50:
            return {"impact": ""}
        try:
            return {"impact": impact_analysis.invoke({"resume_text": state["resume_text"]})}
        except Exception as e:
            return {"impact": f"Impact analysis failed: {str(e)}"}

    def node_review(state):
        context = f"ATS Results:\n{state.get('ats','')}\n\nImpact Results:\n{state.get('impact','')}\n\nResume:\n{state['resume_text'][:2000]}"
        resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=context)])
        return {"messages": [resp]}

    def route(state):
        return "node_impact" if len(state.get("resume_text","")) >= 50 else "node_review"

    g = StateGraph(State)
    g.add_node("node_extract", node_extract)
    g.add_node("node_ats", node_ats)
    g.add_node("node_impact", node_impact)
    g.add_node("node_review", node_review)
    g.set_entry_point("node_extract")
    g.add_edge("node_extract", "node_ats")
    g.add_conditional_edges("node_ats", route, {"node_impact": "node_impact", "node_review": "node_review"})
    g.add_edge("node_impact", "node_review")
    g.add_edge("node_review", END)
    return g.compile()

graph = build_graph()

async def run_resume_reviewer(message: str, history: list[dict]) -> str:
    msgs = [HumanMessage(content=h["content"]) if h["role"]=="user" else AIMessage(content=h["content"]) for h in history]
    msgs.append(HumanMessage(content=message))
    result = await graph.ainvoke({"messages": msgs, "resume_text": "", "ats": "", "impact": ""})
    return result["messages"][-1].content

async def run_resume_reviewer_from_pdf(pdf_bytes: bytes) -> str:
    """Extract text from PDF and run the full review pipeline."""
    text = extract_text_from_pdf(pdf_bytes)
    if not text:
        return "Could not extract text from this PDF. It may be scanned or image-based. Try pasting the resume text directly."
    return await run_resume_reviewer(text, [])