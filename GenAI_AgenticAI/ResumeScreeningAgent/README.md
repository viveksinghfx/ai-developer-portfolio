# 📄 Resume Screening Agent

An agentic resume reviewer built with **LangGraph** that parses resumes (PDF or text), runs ATS keyword scanning, analyzes impact statements, and generates a structured review with actionable improvements — targeted at **AI/ML roles**.

---

## 🚀 Features

- **PDF Parsing** — Extracts text from uploaded PDF resumes via PyPDF2
- **ATS Scanner** — Scores resume against 20+ high-value AI/ML keywords
- **Impact Analyzer** — Detects quantified bullet points and weak action verbs
- **LLM Review** — Structured GPT-4o-mini review with score, analysis, and top 3 improvements
- **Dual Input** — Accepts both raw text and PDF bytes

---

## 🏗️ Architecture

```
Resume (PDF or Text)
        │
        ▼
  node_extract ──→ node_ats ──→ node_impact ──→ node_review
                      │
                      └── (no text?) ──→ node_review directly
```

A **linear LangGraph pipeline** with conditional routing — skips analysis nodes if no resume text is detected.

---

## 📊 Review Output Format

```
## Overall Score (X/10)

## ATS Analysis
ATS Score: XX/100
Found: python, langchain, docker ...
Missing: kubernetes, mlops ...

## Impact Statements
Quantified bullets: X/Y (Z%)
Weak verbs: worked on, helped with ...

## Top 3 Improvements
1. ...
2. ...
3. ...
```

---

## 🛠️ Tech Stack

| Layer | Tech |
|-------|------|
| Agent Framework | LangGraph |
| LLM | OpenAI GPT-4o-mini |
| PDF Parsing | PyPDF2 |
| Language | Python 3.10+ |

---

## ⚙️ Setup

```bash
# 1. Clone the repo
git clone https://github.com/viveksinghfx/resume-screening-agent
cd resume-screening-agent

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY

# 4. Run
python resume_reviewer.py
```

---

## 💬 Usage

**Text input:**
```python
result = await run_resume_reviewer("Paste your resume text here...", history=[])
```

**PDF input:**
```python
with open("resume.pdf", "rb") as f:
    result = await run_resume_reviewer_from_pdf(f.read())
```

---

## 📁 File Structure

```
resume-screening-agent/
├── resume_reviewer.py   # Agent + tools + LangGraph pipeline
├── requirements.txt
├── .env.example
└── README.md
```
