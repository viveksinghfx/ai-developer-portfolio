# Autonomous Codebase Engineer Agent

An agentic AI system built with **LangGraph** that reads any public GitHub repository and implements tasks autonomously — like having a senior engineer who can onboard into any codebase instantly.

## Demo

Live at [viveksingh.tech/demos](https://viveksingh.tech/demos) → Launch **Autonomous Codebase Engineer**

Try it:
```
https://github.com/tiangolo/fastapi  Add rate limiting to all API endpoints
```

---

## How It Works

```
User Input (GitHub URL + task)
        │
        ▼
┌─────────────────┐
│   node_parse    │  Extract repo URL and task from message
└────────┬────────┘
         │
         ▼
┌─────────────────────┐
│ node_fetch_structure│  GitHub API → full file tree (up to 60 files)
└────────┬────────────┘
         │
         ▼
┌─────────────────┐
│  node_analyze   │  Score files by relevance to task keywords
└────────┬────────┘
         │
         ▼
┌──────────────────┐
│ node_read_files  │  Fetch contents of top 3 most relevant files
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ node_implement   │  GPT-4o-mini writes full implementation
└──────────────────┘
```

### Agent Nodes

| Node | Responsibility |
|------|---------------|
| `node_parse` | Extracts GitHub URL and task from the user message |
| `node_fetch_structure` | Calls GitHub API, returns filtered file tree |
| `node_analyze` | Scores files by keyword relevance to the task |
| `node_read_files` | Reads raw contents of top 3 relevant files |
| `node_implement` | Synthesizes complete implementation with diffs |

### Tools

| Tool | What it does |
|------|-------------|
| `fetch_repo_structure` | GitHub Trees API — gets full file tree, filters noise |
| `analyze_task` | Heuristic scorer — matches task keywords to file paths |
| `read_file_from_repo` | GitHub raw content — fetches file contents |

---

## Stack

- **LangGraph** — agent orchestration and state management
- **GPT-4o-mini** — implementation generation
- **GitHub API** — repo structure and file reading (no auth required for public repos)
- **FastAPI** — REST API layer
- **Python 3.12**

---

## Quick Start

```bash
# Clone
git clone https://github.com/viveksinghfx/codebase-engineer
cd codebase-engineer

# Install
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Configure
cp .env.example .env
# Add your OPENAI_API_KEY to .env

# Run
uvicorn app.main:app --reload --port 8000
```

## API Usage

```bash
curl -X POST http://localhost:8000/api/v1/engineer \
  -H "Content-Type: application/json" \
  -d '{
    "message": "https://github.com/tiangolo/fastapi  Add rate limiting to all API endpoints"
  }'
```

**Response:**
```json
{
  "response": "## Task Summary\n...\n## Files to Modify\n...\n## Implementation\n..."
}
```

---

## Project Structure

```
codebase-engineer/
├── app/
│   ├── main.py                          # FastAPI app entry point
│   ├── agents/
│   │   └── codebase_engineer.py         # LangGraph agent + tools
│   └── api/v1/endpoints/
│       └── engineer.py                  # POST /api/v1/engineer endpoint
├── requirements.txt
├── .env.example
└── README.md
```

---

## Example Output

Given: `https://github.com/viveksinghfx/portfolio  Add rate limiting to the agents endpoint`

The agent returns:
- **Task Summary** — what it understood and what it will change
- **Files to Modify** — exact file paths with reasoning
- **Implementation** — complete updated code with inline comments
- **How to Apply** — step-by-step instructions
- **Testing Suggestions** — how to verify the change works

---

## Design Decisions

**Why no GitHub auth?** The agent works on all public repos without requiring users to provide tokens. Adding `Authorization: Bearer <token>` to the request headers in `fetch_repo_structure` extends this to private repos.

**Why 60 file limit?** Context window management. 60 files covers most real-world repos while keeping the file tree readable for the LLM.

**Why read only 3 files?** Each file is truncated at 3000 chars. Reading 3 files = ~9000 tokens of context. Enough to understand the implementation pattern without hitting limits.

**Why GPT-4o-mini?** Cost-effective for this use case. The heavy lifting is done by the structured tools — the LLM only needs to synthesize and write code, not reason from scratch.

---

Built by [Vivek Singh](https://viveksingh.tech)
