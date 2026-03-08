from __future__ import annotations
import json
import re
import urllib.request
from typing import Annotated, TypedDict
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_openai import ChatOpenAI
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages


# ─────────────────────── Tools ───────────────────────

@tool
def fetch_repo_structure(repo_url: str) -> str:
    """Fetch the file tree of a public GitHub repository."""
    try:
        match = re.search(r"github\.com/([^/]+)/([^/\s]+)", repo_url)
        if not match:
            return "Invalid GitHub URL. Format: https://github.com/owner/repo"
        owner, repo = match.group(1), match.group(2).rstrip("/")

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/HEAD?recursive=1"
        req = urllib.request.Request(api_url, headers={"Accept": "application/vnd.github+json"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read())

        files = [item["path"] for item in data.get("tree", []) if item["type"] == "blob"]
        relevant = [f for f in files if not any(skip in f for skip in [
            "node_modules", ".git", "__pycache__", ".next", "dist", "build",
            "pnpm-lock", "package-lock", ".png", ".jpg", ".svg", ".ico", ".woff"
        ])][:60]

        return f"Repository: {owner}/{repo}\nFiles ({len(relevant)} shown):\n" + "\n".join(relevant)
    except Exception as e:
        return f"Could not fetch repo structure: {str(e)}"


@tool
def read_file_from_repo(repo_url: str, file_path: str) -> str:
    """Read the contents of a specific file from a public GitHub repository."""
    try:
        match = re.search(r"github\.com/([^/]+)/([^/\s]+)", repo_url)
        if not match:
            return "Invalid GitHub URL."
        owner, repo = match.group(1), match.group(2).rstrip("/")

        raw_url = f"https://raw.githubusercontent.com/{owner}/{repo}/HEAD/{file_path}"
        req = urllib.request.Request(raw_url)
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")

        if len(content) > 3000:
            content = content[:3000] + f"\n... [truncated, {len(content)} chars total]"
        return f"File: {file_path}\n\n{content}"
    except Exception as e:
        return f"Could not read {file_path}: {str(e)}"


@tool
def analyze_task(task: str, repo_structure: str) -> str:
    """Identify which files need to be changed for the given task."""
    task_lower = task.lower()
    files = repo_structure.split("\n")[2:]

    scored = []
    keywords = task_lower.split()
    for f in files:
        score = 0
        f_lower = f.lower()
        for kw in keywords:
            if kw in f_lower:
                score += 3
        if any(x in f_lower for x in ["main", "index", "app", "router", "api", "endpoint"]):
            score += 1
        if any(x in f_lower for x in ["test", "spec"]):
            score += 2 if "test" in task_lower else 0
        if score > 0:
            scored.append((score, f))

    scored.sort(reverse=True)
    top = [f for _, f in scored[:8]]

    return (
        f"Task analysis: '{task}'\n\n"
        f"Most relevant files to modify:\n" +
        "\n".join(f"  - {f}" for f in top) +
        ("\n\nNo strongly matching files found — may need new files." if not top else "")
    )


# ─────────────────────── State ───────────────────────

class State(TypedDict):
    messages: Annotated[list, add_messages]
    repo_url: str
    task: str
    repo_structure: str
    relevant_files: str
    file_contents: str
    step: int


SYSTEM = """You are an Autonomous Codebase Engineer. You analyse GitHub repositories and implement tasks like a senior engineer.

When given a repo + task, you:
1. Understand the codebase architecture from the file tree
2. Identify exactly which files need changes
3. Write complete, production-ready code implementations
4. Explain every change with reasoning

Format your response as:
## Task Summary
## Files to Modify
## Implementation
For each file: show the complete updated code block with clear before/after diffs in comments
## How to Apply These Changes
## Testing Suggestions

Be specific, write actual code — not pseudocode."""


# ─────────────────────── Graph ───────────────────────

def build_graph():
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.1)

    def node_parse(state):
        last = next((m for m in reversed(state["messages"]) if isinstance(m, HumanMessage)), None)
        content = last.content if last else ""

        url_match = re.search(r"https?://github\.com/[^\s]+", content)
        repo_url = url_match.group(0).rstrip(".,") if url_match else ""

        if repo_url:
            task = content.replace(repo_url, "").strip().lstrip(":-").strip()
        else:
            task = content

        return {"repo_url": repo_url, "task": task, "step": 0}

    def node_fetch_structure(state):
        if not state.get("repo_url"):
            return {"repo_structure": "No GitHub URL provided."}
        result = fetch_repo_structure.invoke({"repo_url": state["repo_url"]})
        return {"repo_structure": result}

    def node_analyze(state):
        if not state.get("task") or "No GitHub URL" in state.get("repo_structure", ""):
            return {"relevant_files": ""}
        result = analyze_task.invoke({
            "task": state["task"],
            "repo_structure": state["repo_structure"]
        })
        return {"relevant_files": result}

    def node_read_files(state):
        relevant = state.get("relevant_files", "")
        repo_url = state.get("repo_url", "")
        if not relevant or not repo_url:
            return {"file_contents": ""}

        paths = re.findall(r"- (.+)", relevant)[:3]
        contents = []
        for path in paths:
            content = read_file_from_repo.invoke({"repo_url": repo_url, "file_path": path.strip()})
            contents.append(content)

        return {"file_contents": "\n\n---\n\n".join(contents)}

    def node_implement(state):
        if not state.get("repo_url"):
            resp = llm.invoke([
                SystemMessage(content=SYSTEM),
                HumanMessage(content=(
                    f"The user asked: {state.get('task', '')}\n\n"
                    "No GitHub URL was provided. Ask them to share a public GitHub repo URL "
                    "along with the task, like:\n"
                    "https://github.com/username/repo  Add rate limiting to all API endpoints"
                ))
            ])
            return {"messages": [resp]}

        context = (
            f"Repository Structure:\n{state.get('repo_structure', '')}\n\n"
            f"Task Analysis:\n{state.get('relevant_files', '')}\n\n"
            f"Key File Contents:\n{state.get('file_contents', '')}\n\n"
            f"Task to implement: {state.get('task', '')}"
        )

        resp = llm.invoke([SystemMessage(content=SYSTEM), HumanMessage(content=context)])
        return {"messages": [resp]}

    def route(state):
        return "node_fetch_structure" if state.get("repo_url") else "node_implement"

    g = StateGraph(State)
    g.add_node("node_parse", node_parse)
    g.add_node("node_fetch_structure", node_fetch_structure)
    g.add_node("node_analyze", node_analyze)
    g.add_node("node_read_files", node_read_files)
    g.add_node("node_implement", node_implement)

    g.set_entry_point("node_parse")
    g.add_conditional_edges("node_parse", route, {
        "node_fetch_structure": "node_fetch_structure",
        "node_implement": "node_implement",
    })
    g.add_edge("node_fetch_structure", "node_analyze")
    g.add_edge("node_analyze", "node_read_files")
    g.add_edge("node_read_files", "node_implement")
    g.add_edge("node_implement", END)

    return g.compile()


graph = build_graph()


async def run_codebase_engineer(message: str, history: list[dict]) -> str:
    msgs = [
        HumanMessage(content=h["content"]) if h["role"] == "user"
        else AIMessage(content=h["content"])
        for h in history
    ]
    msgs.append(HumanMessage(content=message))
    result = await graph.ainvoke({
        "messages": msgs,
        "repo_url": "",
        "task": "",
        "repo_structure": "",
        "relevant_files": "",
        "file_contents": "",
        "step": 0,
    })
    return result["messages"][-1].content
