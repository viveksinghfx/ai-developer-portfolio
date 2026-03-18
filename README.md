<div align="center">

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:1d4ed8,100:7c3aed&height=200&section=header&text=Vivek%20Singh&fontSize=50&fontColor=ffffff&animation=fadeIn&fontAlignY=35&desc=Agentic%20AI%20%E2%80%A2%20GenAI%20Architecture%20%E2%80%A2%20LLM%20Systems&descAlignY=55&descSize=18" alt="header"/>

[![Portfolio](https://img.shields.io/badge/Portfolio-viveksingh.tech-1d4ed8?style=for-the-badge&logo=vercel&logoColor=white)](https://viveksingh.tech)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/vivek-singh-633886137/)
[![DataCamp](https://img.shields.io/badge/DataCamp-Certified-03EF62?style=for-the-badge&logo=datacamp&logoColor=white)](https://www.datacamp.com/portfolio/acevivek)
[![GitHub](https://img.shields.io/github/stars/viveksinghfx/ai-developer-portfolio?style=for-the-badge&logo=github&color=ffd700)](https://github.com/viveksinghfx/ai-developer-portfolio)

<br/>

> **"A Houdini network and a LangGraph are the same data structure — a directed graph of composable nodes.**
> **I switched from simulating fire to orchestrating reasoning."**

<br/>

![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)
![LangGraph](https://img.shields.io/badge/LangGraph-FF6B6B?style=flat-square&logo=chainlink&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-1C3C3C?style=flat-square&logo=chainlink&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=flat-square&logo=fastapi&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-FF9900?style=flat-square&logo=amazonaws&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=flat-square&logo=docker&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=flat-square&logo=openai&logoColor=white)
![Next.js](https://img.shields.io/badge/Next.js-000000?style=flat-square&logo=nextdotjs&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?style=flat-square&logo=postgresql&logoColor=white)
![Terraform](https://img.shields.io/badge/Terraform-7B42BC?style=flat-square&logo=terraform&logoColor=white)

</div>

---

## 👋 Who I Am

I'm **Vivek Singh** — an **Agentic AI & GenAI Engineer** who spent 3 years building procedural FX pipelines for Hollywood productions *(Transformers, Ant-Man, Crater)* at Technicolor India and Harikatha Studio, and pivoted that exact systems-thinking discipline into production AI architecture.

This is not a tutorial repo. Every project here is **live, deployed, and serving real traffic** on AWS infrastructure.

---

## 🚀 Live System — viveksingh.tech

Five production LangGraph agents running on AWS ECS Fargate right now. No mocks. No demos. Actually callable.

<table>
<tr>
<td width="50%">

### 🤖 Portfolio Chat Agent
RAG pipeline that answers questions about my background, projects, and stack using semantic retrieval over my portfolio content.

**Stack:** FAISS · OpenAI Embeddings · LangGraph  
**Retrieval:** Top-3 chunk injection, answers grounded in context only

</td>
<td width="50%">

### 📄 Resume Reviewer
ATS-style scorer with structured feedback across 5 dimensions. Accepts PDF or pasted text.

**Stack:** OpenAI · Pydantic · FastAPI  
**Output:** Validated JSON score + per-section improvement suggestions

</td>
</tr>
<tr>
<td width="50%">

### 🔬 Multi-Agent Research System
Multi-step research pipeline with self-correction loops. Routes back to search if confidence is below threshold.

**Stack:** LangGraph StateGraph · GPT-4o  
**Pattern:** Conditional edges, confidence-based routing, up to 3 self-correction loops

</td>
<td width="50%">

### 📈 Finance AI Agent
Market analysis agent covering US equities and Indian markets (NSE/BSE).

**Stack:** LangGraph · Market data tools  
**Coverage:** Real-time US stocks + NSE/BSE tickers with trend analysis

</td>
</tr>
<tr>
<td colspan="2">

### ⚙️ Autonomous Codebase Engineer
Give it any public GitHub repo URL and a plain-English task. It reads the repo structure, scores files by relevance, reads the key ones, and writes a complete implementation with diffs.

**Architecture:** 5-node LangGraph pipeline — `parse → fetch_structure → analyze → read_files → implement`  
**Tools:** GitHub API (repo tree), raw.githubusercontent.com (file content), heuristic file scorer  
**Context management:** 60-file cap, 3000-char truncation per file  
**Model:** GPT-4o-mini (optimised cost/quality tradeoff for code generation tasks)

</td>
</tr>
</table>

---

## 🏗️ Production Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                        viveksingh.tech                              │
│                     (Next.js + CloudFront)                          │
└──────────────────────────────┬──────────────────────────────────────┘
                               │ HTTPS
                               ▼
                    ┌──────────────────┐
                    │  Application     │
                    │  Load Balancer   │
                    └────────┬─────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
     ┌─────────────┐ ┌─────────────┐ ┌─────────────┐
     │  FastAPI    │ │  FastAPI    │ │  FastAPI    │
     │  Agent 1   │ │  Agent 2   │ │  Agent N   │
     │ (ECS Task) │ │ (ECS Task) │ │ (ECS Task) │
     └──────┬──────┘ └──────┬──────┘ └──────┬──────┘
            │               │               │
            └───────────────┼───────────────┘
                            │
              ┌─────────────┼─────────────┐
              ▼             ▼             ▼
     ┌──────────────┐ ┌──────────┐ ┌──────────┐
     │  PostgreSQL  │ │  FAISS   │ │   S3     │
     │  (RDS)       │ │ Vectors  │ │ Storage  │
     └──────────────┘ └──────────┘ └──────────┘
            │
            ▼
     ┌──────────────┐
     │  OpenAI API  │
     │  (GPT-4o)    │
     └──────────────┘
```

**AWS Services in use:**
`ECS Fargate` · `ALB` · `ECR` · `RDS (PostgreSQL)` · `S3` · `Amplify` · `CloudFront` · `ACM` · `Route 53`

---

## 📂 Repository Structure

```
ai-developer-portfolio/
│
├── GenAI_AgenticAI/
│   ├── MultiAgentResearch/           # LangGraph research pipeline with self-correction
│   ├── PortfolioChatAgent/           # RAG-based Q&A over portfolio content
│   ├── ResumeScreeningAgent/         # ATS resume reviewer with Pydantic validation
│   ├── FinanceAiAgent/               # US + NSE/BSE market analysis agent
│   └── AutonomousCodebaseEngineer/   # GitHub repo reader + code implementation agent
│
├── MachineLearningProjects/          # Classical ML, DL, and NLP experiments
│
├── .gitignore
└── README.md
```

---

## 🤖 GenAI & Agentic AI — Deep Dive

### ⚙️ Autonomous Codebase Engineer

> Give it a GitHub URL and a task in plain English. It reads, reasons, and writes code.

**How it works:**

```
User Input (repo URL + task)
        │
        ▼
[Node 1: parse]          Extract owner/repo from URL
        │
        ▼
[Node 2: fetch_structure] GitHub API → full repo file tree
        │
        ▼
[Node 3: analyze]        Score files by relevance to task
                         (heuristic scorer, top 60 files)
        │
        ▼
[Node 4: read_files]     Fetch content of scored files
                         (3000-char truncation per file)
        │
        ▼
[Node 5: implement]      GPT-4o-mini generates full implementation
                         with diffs and explanation
        │
        ▼
Structured output (code + reasoning)
```

**Key design decisions:**
- 60-file cap prevents context overflow while covering most real-world repos
- File scoring avoids sending irrelevant files (tests, configs, docs) to the LLM
- GPT-4o-mini chosen over GPT-4o for this node — code generation quality is comparable at 10× lower cost

---

### 🔬 Multi-Agent Research System

> Searches, evaluates, self-corrects, and produces structured reports with source attribution.

```
Query Input
    │
    ▼
[search_agent]    Web search + source gathering
    │
    ▼
[evaluate]        Confidence scoring of results
    │
    ├── confidence ≥ threshold ──────────────────────────► [synthesize]
    │                                                           │
    └── confidence < threshold (retry ≤ 3)                     ▼
            │                                         Structured report
            └──────────────────────────────────────► [output]
```

**Self-correction loop:** If search results score below the confidence threshold, the agent reformulates the query and searches again — up to 3 attempts before proceeding with the best available result.

---

### 💬 Portfolio Chat Agent (RAG)

> Semantic retrieval over portfolio content. Answers grounded strictly in context.

| Component | Choice | Why |
|---|---|---|
| Chunking | RecursiveCharacterTextSplitter | Preserves semantic boundaries better than fixed-size |
| Chunk size | 512 tokens, 50-token overlap | Balances context richness vs retrieval precision |
| Embeddings | `text-embedding-3-small` | Best cost/quality for semantic search |
| Vector store | FAISS | In-memory, zero-latency for portfolio scale |
| Retrieval | Top-3 chunks | Enough context without diluting relevance |
| Grounding | Answers ONLY from retrieved context | Eliminates hallucination on personal facts |

---

### 📄 Resume Screening Agent

> ATS-style scoring with structured Pydantic output and actionable per-section feedback.

**Scoring dimensions:**

| Dimension | What It Checks |
|---|---|
| Keyword Match | Alignment with job description terminology |
| Formatting | ATS-parseable structure, no tables/columns/images |
| Quantified Achievements | Numbers, percentages, scale indicators |
| Action Verbs | Strong opening verbs per bullet point |
| Length & Density | Appropriate length for experience level |

**Output:** Pydantic-validated JSON — guaranteed schema, no free-form text parsing needed downstream.

---

## 🛠️ Full Tech Stack

<table>
<tr><th>Category</th><th>Technologies</th></tr>
<tr>
<td><b>Languages</b></td>
<td>Python · TypeScript · JavaScript · SQL · Bash</td>
</tr>
<tr>
<td><b>AI / Agents</b></td>
<td>LangGraph · LangChain · LlamaIndex · OpenAI · Llama 3 · Hugging Face</td>
</tr>
<tr>
<td><b>ML / DL</b></td>
<td>scikit-learn · PyTorch · TensorFlow · Keras · XGBoost</td>
</tr>
<tr>
<td><b>Vector / Search</b></td>
<td>FAISS · Pinecone · OpenAI Embeddings · Hybrid BM25 + Vector</td>
</tr>
<tr>
<td><b>Backend</b></td>
<td>FastAPI · SQLAlchemy · PostgreSQL · JWT Auth · Pydantic</td>
</tr>
<tr>
<td><b>Frontend</b></td>
<td>Next.js · React · Tailwind CSS</td>
</tr>
<tr>
<td><b>AWS</b></td>
<td>ECS Fargate · ALB · ECR · RDS · S3 · Amplify · CloudFront · ACM · Route 53</td>
</tr>
<tr>
<td><b>Infrastructure</b></td>
<td>Docker · Docker Compose · Kubernetes · Terraform · GitHub Actions</td>
</tr>
<tr>
<td><b>Data</b></td>
<td>pandas · NumPy · Seaborn · Matplotlib</td>
</tr>
<tr>
<td><b>NLP / Vision</b></td>
<td>Transformers · Image Processing · OCR · Sentiment Analysis</td>
</tr>
<tr>
<td><b>MLOps</b></td>
<td>MLOps Concepts · Explainable AI · Responsible AI · Hyperparameter Tuning</td>
</tr>
</table>

---

## 🧠 The FX → AI Parallel (Why This Background is an Advantage)

Three years of pipeline engineering maps directly to modern AI systems. The vocabulary changed. The thinking did not.

| VFX Pipeline | AI System | Shared Principle |
|---|---|---|
| Houdini SOP Network | LangGraph StateGraph | Directed graph of composable, stateless nodes |
| VEX Kernels | LLM Tool Functions | Atomic, typed, side-effect-free compute units |
| Procedural Simulation | RAG Pipeline | Parameterised, reproducible, modular processing |
| Unreal Blueprints | Agent Conditional Edges | Event-driven state transitions between nodes |
| Realtime VFX (<16ms) | Production LLM API (<500ms) | Performance-first: cache, batch, optimise hot paths |
| Asset Pipeline Automation | ML Data Pipeline | ETL with domain-specific transforms |

Same data structures. Same systems thinking. Same Python. Different domain.

---

## 💼 Experience

**Technical FX Artist** — *Harikatha Studio Pvt Ltd* *(Nov 2023 – Present)*
Production FX pipeline automation · Tool scripting in Python/VEX · Rendering system optimisation · Production debugging under hard deadlines

**Technical FX Artist** — *Technicolor India Private Limited* *(Jul 2022 – Sep 2023)*
FX pipeline development for Hollywood VFX productions · Python automation tooling · Cross-team collaboration
*Credits: Transformers · Ant-Man · Crater*

---

## 📜 Certifications

| Certification | Issuer |
|---|---|
| 🏅 AI Engineer for Developers Associate | DataCamp |
| 🏅 Python Data Associate | DataCamp |

---

## 📚 Learning Path

<details>
<summary><b>🐍 Python & Data Foundations</b></summary>

`Introduction to Python` · `Intermediate Python` · `Intermediate Python for Developers` · `Introduction to Statistics` · `Hypothesis Testing in Python` · `Introduction to Git`

</details>

<details>
<summary><b>📊 Data Engineering & Analysis</b></summary>

`Data Manipulation with pandas` · `Cleaning Data in Python` · `Introduction to Data Visualization with Seaborn` · `Feature Engineering for Machine Learning in Python` · `Introduction to APIs in Python`

</details>

<details>
<summary><b>🤖 Machine Learning</b></summary>

`Supervised Learning with scikit-learn` · `Unsupervised Learning in Python` · `Ensemble Methods in Python` · `Hyperparameter Tuning in Python` · `Designing Machine Learning Workflows in Python`

</details>

<details>
<summary><b>🧠 Deep Learning</b></summary>

`Introduction to Deep Learning in Python` · `Introduction to Deep Learning with PyTorch` · `Intermediate Deep Learning with PyTorch` · `Introduction to TensorFlow in Python` · `Image Processing in Python` · `Image Modeling with Keras`

</details>

<details>
<summary><b>🦾 LLMs & Generative AI</b></summary>

`Introduction to LLMs in Python` · `Developing LLM Applications with LangChain` · `Multi-Agent Systems with LangGraph` · `Building Scalable Agentic Systems` · `Working with Hugging Face` · `Working with Llama 3`

</details>

<details>
<summary><b>⚙️ MLOps & Production</b></summary>

`Introduction to FastAPI` · `MLOps Concepts` · `Responsible AI Data Management` · `Explainable AI in Python` · `Data Structures and Algorithms in Python`

</details>

---

## 🚀 Getting Started

To run any agent locally:

```bash
# 1. Clone the repo
git clone https://github.com/viveksinghfx/ai-developer-portfolio.git
cd ai-developer-portfolio

# 2. Navigate to any agent
cd GenAI_AgenticAI/MultiAgentResearch   # or any other agent folder

# 3. Create a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Set environment variables
cp .env.example .env
# Add your OPENAI_API_KEY and any other required keys

# 6. Run
python main.py
# or: uvicorn app:app --reload  (for FastAPI agents)
```

> **Note:** Each project folder contains its own `requirements.txt` and `.env.example`. Check the project-level README for specific setup instructions.

---

## 📬 Contact & Opportunities

I'm currently open to roles in:
- **Agentic AI Engineering** — building multi-agent systems at production scale
- **GenAI Architecture** — designing LLM pipelines, RAG systems, and AI infrastructure
- **LLM Systems Engineering** — model serving, MLOps, AI-powered product development

<div align="center">

| Channel | Link |
|---|---|
| 🌐 Portfolio | [viveksingh.tech](https://viveksingh.tech) |
| 💼 LinkedIn | [linkedin.com/in/vivek-singh-633886137](https://www.linkedin.com/in/vivek-singh-633886137/) |
| 📧 Email | [hello@viveksingh.tech](mailto:hello@viveksingh.tech) |
| 📊 DataCamp | [datacamp.com/portfolio/acevivek](https://www.datacamp.com/portfolio/acevivek) |

<br/>

<img src="https://capsule-render.vercel.app/api?type=waving&color=0:7c3aed,100:1d4ed8&height=100&section=footer" alt="footer"/>

*Built with production discipline — not just tutorial code.*

</div>
