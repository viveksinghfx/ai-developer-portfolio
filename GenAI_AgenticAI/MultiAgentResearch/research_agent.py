from __future__ import annotations
from typing import Annotated, Literal, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages
import json

try:
    from langchain_community.tools import DuckDuckGoSearchRun
    _ddg = DuckDuckGoSearchRun()
    @tool
    def web_search(query: str) -> str:
        """Search the web for current information."""
        try: return _ddg.run(query)
        except Exception as e: return f"Search error: {e}"
except Exception:
    @tool
    def web_search(query: str) -> str:
        """Search the web for current information."""
        return f"Simulated search for: {query}. In production this connects to DuckDuckGo."

@tool
def decompose_query(question: str) -> str:
    """Break a research question into specific sub-questions."""
    return json.dumps({
        "sub_questions": [
            f"What is the current state of {question}?",
            f"What are the key challenges in {question}?",
            f"What are recent developments in {question}?",
            f"What are practical applications of {question}?",
        ],
        "search_queries": [f"{question} 2024", f"{question} latest", f"{question} examples"]
    })

class State(TypedDict):
    messages: Annotated[list, add_messages]
    step_count: int

SYSTEM = """You are an autonomous research AI agent. For any topic:
1. Use decompose_query to break it into sub-questions
2. Use web_search 2-3 times with specific queries
3. Synthesize into a structured report:
   - Executive Summary (2-3 sentences)
   - Key Findings (3-5 bullets)
   - Challenges
   - Applications
Show your reasoning at each step."""

def build_graph():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)
    tools = [decompose_query, web_search]
    llm_wt = llm.bind_tools(tools)
    tbn = {t.name: t for t in tools}

    def agent(state):
        resp = llm_wt.invoke([SystemMessage(content=SYSTEM)] + state["messages"])
        return {"messages": [resp], "step_count": state.get("step_count", 0) + 1}

    def tool_node(state):
        last = state["messages"][-1]
        return {"messages": [ToolMessage(content=str(tbn[tc["name"]].invoke(tc["args"])), tool_call_id=tc["id"]) for tc in last.tool_calls if tc["name"] in tbn]}

    def route(state) -> Literal["tools", "__end__"]:
        last = state["messages"][-1]
        if state.get("step_count", 0) >= 6: return END
        return "tools" if getattr(last, "tool_calls", None) else END

    g = StateGraph(State)
    g.add_node("agent", agent); g.add_node("tools", tool_node)
    g.set_entry_point("agent")
    g.add_conditional_edges("agent", route, {"tools": "tools", END: END})
    g.add_edge("tools", "agent")
    return g.compile()

graph = build_graph()

async def run_research_agent(message: str, history: list[dict]) -> str:
    msgs = [HumanMessage(content=h["content"]) if h["role"]=="user" else AIMessage(content=h["content"]) for h in history]
    msgs.append(HumanMessage(content=message))
    result = await graph.ainvoke({"messages": msgs, "step_count": 0})
    return result["messages"][-1].content
