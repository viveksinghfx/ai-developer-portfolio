# 👋 Hi, I'm Vivek Singh

**AI/ML Engineer** · Former Technical FX Artist @ Technicolor India & Harikatha Studio  
Transitioning from 3 years of VFX pipeline engineering into production-grade AI systems.

[![Portfolio](https://img.shields.io/badge/Portfolio-viveksingh.tech-blue?style=for-the-badge&logo=vercel)](https://viveksingh.tech)
[![DataCamp](https://img.shields.io/badge/DataCamp-Certified-03EF62?style=for-the-badge&logo=datacamp)](https://www.datacamp.com/portfolio/acevivek)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Connect-0A66C2?style=for-the-badge&logo=linkedin)](https://www.linkedin.com/in/vivek-singh-633886137/)

---

## 🚀 Live Portfolio — viveksingh.tech

A production-grade full-stack AI system running **5 live LangGraph agents** on AWS.

> **Not a demo. Not a mock. Actually deployed and testable right now.**

| Agent | What it does |
|-------|-------------|
| 🤖 **Portfolio Chat** | RAG agent — answers questions about my projects using semantic retrieval |
| 📄 **Resume Reviewer** | ATS scorer with structured feedback per section |
| 🔬 **Research Agent** | Multi-step research with self-correction loops |
| 📈 **Finance Agent** | US and Indian market analysis |
| ⚙️ **Codebase Engineer** | Give it any public GitHub repo + a task → writes the full implementation |

**Stack:** FastAPI · LangGraph · PostgreSQL · Next.js · Docker  
**AWS:** ECS Fargate · ALB · ECR · RDS · Amplify · CloudFront · ACM · Route53

---

## 📂 Repository Structure

```
Project/
└── GenAI_AgenticAI/
    ├── MultiAgentResearch/          # Multi-step research agent with self-correction
    ├── PortfolioChatAgent/          # RAG-based portfolio chat
    ├── ResumeScreeningAgent/        # ATS resume reviewer
    ├── FinanceAiAgent/              # US + Indian market finance agent
    └── AutonomousCodebaseEngineer/  # GitHub repo reader + code implementer
```

---

## 🤖 GenAI & Agentic AI Projects

### ⚙️ [Autonomous Codebase Engineer](./GenAI_AgenticAI/AutonomousCodebaseEngineer)
Give it a GitHub URL and a plain-English task. It reads the repo structure, scores files by relevance, reads key files, and writes a complete implementation with diffs.

- **Architecture:** 5-node LangGraph pipeline (`parse → fetch_structure → analyze → read_files → implement`)
- **Tools:** GitHub API (repo tree), raw.githubusercontent.com (file content), heuristic file scorer
- **Context management:** 60-file cap, 3000-char truncation per file
- **Model:** GPT-4o-mini (cost/quality tradeoff for code generation)

### 🔬 [Multi-Agent Research System](./GenAI_AgenticAI/MultiAgentResearch)
Multi-step research agent that searches, evaluates confidence, and self-corrects when results are weak.

- **Architecture:** LangGraph StateGraph with conditional routing
- **Self-correction loop:** If search confidence < threshold, loops back up to 3 times
- **Output:** Structured research report with source attribution

### 💬 [Portfolio Chat Agent (RAG)](./GenAI_AgenticAI/PortfolioChatAgent)
RAG pipeline that answers questions about my projects using semantic retrieval.

- **Chunking:** RecursiveCharacterTextSplitter — 512 tokens, 50-token overlap
- **Embedding:** OpenAI text-embedding-3-small
- **Vector store:** FAISS for similarity search
- **Retrieval:** Top-3 chunks injected as context, model answers ONLY from context

### 📄 [Resume Screening Agent](./GenAI_AgenticAI/ResumeScreeningAgent)
ATS-style resume reviewer with structured scoring across 5 dimensions.

- **Dimensions:** Keyword match · Formatting · Quantified achievements · Action verbs · Length
- **Output:** Pydantic-validated JSON score + per-section improvement suggestions
- **Accepts:** PDF upload or pasted text

### 📈 [Finance AI Agent](./GenAI_AgenticAI/FinanceAiAgent)
Financial analysis agent covering US stocks and Indian markets (NSE/BSE).

- **Tools:** Market data retrieval, trend analysis, comparison
- **Coverage:** US equities + NSE/BSE tickers

---

## 🛠️ Tech Stack

```
Languages        Python · JavaScript · TypeScript · SQL
AI / Agents      LangGraph · LangChain · LlamaIndex · OpenAI · Llama 3 · Hugging Face
ML / DL          scikit-learn · PyTorch · TensorFlow · Keras · XGBoost
Data             pandas · NumPy · Seaborn · Matplotlib · Feature Engineering
NLP / Vision     Transformers · Image Processing · OCR · Sentiment Analysis
Backend          FastAPI · SQLAlchemy · PostgreSQL · JWT · Docker
Frontend         Next.js · React · Tailwind CSS
Vector / Search  FAISS · Embeddings · RAG pipelines
AWS              ECS Fargate · ALB · ECR · RDS · Amplify · CloudFront · ACM
MLOps            MLOps Concepts · Explainable AI · Responsible AI · Hyperparameter Tuning
Tools            Git · Docker Compose · GitHub Actions
```

---

## 📜 Certifications

- 🏅 **AI Engineer for Developers Associate** — DataCamp
- 🏅 **Python Data Associate** — DataCamp

---

## 🎓 Courses Completed

A structured learning path from Python fundamentals to production AI systems.

**🐍 Python & Data Foundations**
`Introduction to Python` · `Intermediate Python` · `Intermediate Python for Developers` · `Introduction to Statistics` · `Hypothesis Testing in Python` · `Introduction to Git`

**📊 Data Engineering & Analysis**
`Data Manipulation with pandas` · `Cleaning Data in Python` · `Introduction to Data Visualization with Seaborn` · `Feature Engineering for Machine Learning in Python` · `Introduction to APIs in Python`

**🤖 Machine Learning**
`Supervised Learning with scikit-learn` · `Unsupervised Learning in Python` · `Ensemble Methods in Python` · `Hyperparameter Tuning in Python` · `Designing Machine Learning Workflows in Python`

**🧠 Deep Learning**
`Introduction to Deep Learning in Python` · `Introduction to Deep Learning with PyTorch` · `Intermediate Deep Learning with PyTorch` · `Introduction to TensorFlow in Python` · `Image Processing in Python` · `Image Modeling with Keras`

**🦾 LLMs & Generative AI**
`Introduction to LLMs in Python` · `Developing LLM Applications with LangChain` · `Multi-Agent Systems with LangGraph` · `Building Scalable Agentic Systems` · `Working with Hugging Face` · `Working with Llama 3`

**⚙️ MLOps & Production**
`Introduction to FastAPI` · `MLOps Concepts` · `Responsible AI Data Management` · `Explainable AI in Python` · `Data Structures and Algorithms in Python`

---

## 💼 Experience

**Technical FX Artist** · Harikatha Studio Pvt Ltd *(Nov 2023 – Present)*  
Automation scripting · Pipeline tooling · Rendering systems · Production debugging

**Technical FX Artist** · Technicolor India Private Limited *(Jul 2022 – Sep 2023)*  
FX pipeline development · Tool scripting · Cross-team collaboration under production deadlines

---

## 📬 Let's Connect

- 🌐 **Portfolio:** [viveksingh.tech](https://viveksingh.tech)
- 💼 **LinkedIn:** [linkedin.com/in/vivek-singh-633886137](https://www.linkedin.com/in/vivek-singh-633886137/)
- 📊 **DataCamp:** [datacamp.com/portfolio/acevivek](https://www.datacamp.com/portfolio/acevivek)

---

<p align="center">
  <i>Built with production discipline — not just tutorial code.</i>
</p>
