# TCS_AMD_Hackthon
A repo for the Hackthon
# ModernizeIQ — TCS × AMD AI Hackathon Edition

> A multi-agent AI advisor that analyzes a portfolio of enterprise applications and tells you — for each one — **what to do with it, why, and in what order.** Powered by open-source LLMs running on AMD GPUs.

**Track:** Track 1 — Agents
**Use Case:** AGENTS_026 (Autonomous Incident Diagnosis) — adapted as enterprise application modernization intelligence
**Team:** Rohith ( Agents + RAG), Sumedh (Dev · Data + Retrieval), Mahesh (Story + Demo)

---

## TL;DR

- **Input:** 5 synthetic enterprise applications — each with tech stack, age, CVE count, dependencies, business criticality.
- **Brain:** 3 CrewAI agents in sequence — one scores risk, one picks the modernization decision (grounded in a retrieved knowledge base via RAG), one explains it in plain English.
- **Knowledge Base:** ~15 curated modernization patterns embedded into ChromaDB. The decision agent retrieves the most relevant patterns before deciding — so every recommendation is grounded in real-world practice, not model memory.
- **Output:** A Streamlit dashboard showing each app's risk score, its 6R recommendation, the patterns it was grounded in, and a plain-language explanation.
- **AMD angle:** Every analysis fires embedding inference (retrieval) + LLM inference (reasoning) — two distinct GPU workloads. Scale to a 500-app enterprise portfolio and you have a serious, continuous AMD compute workload.

---

## The Problem

Most large enterprises run on software built 10–20 years ago. It still works, barely — but operating systems are unsupported, security risks are compounding, and maintenance costs keep climbing. Every one of these systems eventually has to be modernized: moved to the cloud, redesigned, replaced, or retired.

The hard part isn't doing the work. It's **deciding what to do.**

A typical enterprise has 500–5,000 applications. For each one, someone has to answer: *Is this worth keeping? Move it as-is, redesign it, or kill it? What breaks if we touch it? When?*

Today this is done by consultants over months, costs millions, and produces a static report that's stale the day it lands. **ModernizeIQ replaces that analysis with a three-agent AI pipeline that does it in minutes, grounded in known patterns, with full reasoning visible.**

---

## The 6R Framework

ModernizeIQ picks one of six standard modernization decisions for every application:

| Decision | What it means |
|----------|---------------|
| **Rehost** | Move to cloud as-is ("lift and shift") |
| **Replatform** | Move with minor changes (e.g., managed database) |
| **Refactor** | Significantly redesign for the cloud |
| **Retire** | Shut it down — not worth keeping |
| **Replace** | Swap for an off-the-shelf product |
| **Retain** | Leave it alone for now |

Choosing wrong is expensive. Rehosting something that should have been retired wastes months. ModernizeIQ makes this call **defensibly, with evidence.**

---

## How It Works

```
  ┌──────────────────┐
  │  5 Synthetic     │
  │  App Records     │
  │  (JSON)          │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐        ┌──────────────────────┐
  │  Assessment      │        │                      │
  │  Agent           │        │   Knowledge Base     │
  │                  │        │   ~15 modernization  │
  │  → risk score    │        │   patterns           │
  │    (0–100)       │        │   (ChromaDB)         │
  └────────┬─────────┘        └──────────┬───────────┘
           │                             │
           ▼                             │ retrieves top-3
  ┌──────────────────┐                   │ relevant patterns
  │  6R Decision     │◄──────────────────┘
  │  Agent  (RAG)    │
  │                  │
  │  → 6R decision   │
  │  → confidence    │
  │  → patterns used │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  Explanation     │
  │  Agent           │
  │                  │
  │  → plain-English │
  │    reasoning a   │
  │    manager reads │
  └────────┬─────────┘
           │
           ▼
  ┌──────────────────┐
  │  Streamlit       │
  │  Dashboard       │
  │                  │
  │  portfolio view  │
  │  score · 6R tag  │
  │  patterns · why  │
  └──────────────────┘
```

**Why three agents instead of one big prompt:**
A single mega-prompt is a black box — when it's wrong, you can't tell which part failed. Three focused agents each have one job, can be tested independently, and can be improved one at a time.

**Why RAG instead of just asking the model:**
Without retrieval, the model recommends from memory. With retrieval, every recommendation is grounded in a curated set of real modernization patterns — and we can *show* which patterns drove each decision. That's the difference between "the AI said so" and "here's the prior practice this is based on."

---

## Architecture

```
┌─────────────────────────────────────────────────┐
│             FRONTEND                             │
│         Streamlit Dashboard                      │
│  portfolio table · risk scores · 6R badges      │
│  retrieved patterns · plain-language reasoning  │
└────────────────────┬────────────────────────────┘
                     │ HTTP (JSON)
                     ▼
┌─────────────────────────────────────────────────┐
│              API LAYER                           │
│           FastAPI (Python)                       │
│    POST /analyze → runs crew → returns report   │
└────────────────────┬────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│          AI REASONING LAYER (CrewAI)             │
│                                                  │
│  ┌─────────────┐  ┌──────────────┐  ┌─────────┐ │
│  │ Assessment  │→ │ 6R Decision  │→ │ Explain │ │
│  │   Agent     │  │ Agent + RAG  │  │  Agent  │ │
│  └─────────────┘  └──────┬───────┘  └─────────┘ │
│                           │ retrieve             │
│                           ▼                      │
│                  ┌─────────────────┐             │
│                  │   ChromaDB      │             │
│                  │ + embeddings    │             │
│                  │ (knowledge base)│             │
│                  └─────────────────┘             │
│                           │                      │
│                           ▼ LLM calls            │
│                  ┌─────────────────┐             │
│                  │  Llama 3.1 8B   │             │
│                  │  via Ollama     │             │
│                  │  (AMD MI300X)   │             │
│                  └─────────────────┘             │
└─────────────────────────────────────────────────┘
                     │
                     ▼
┌─────────────────────────────────────────────────┐
│              DATA LAYER                          │
│  synthetic_apps.json  → 5 sample applications   │
│  knowledge_base/      → 15 markdown pattern docs│
└─────────────────────────────────────────────────┘
```

---

## Technology Stack

| Layer | Technology | Why |
|-------|------------|-----|
| Frontend | Streamlit | Fast to build, perfect for demo, no build step |
| API | FastAPI (Python) | Same language as AI layer, clean REST |
| AI Orchestration | CrewAI | Purpose-built multi-agent framework |
| LLM | Llama 3.1 8B via Ollama | Open-source, runs on AMD ROCm, fast enough |
| Embeddings | sentence-transformers (all-MiniLM-L6-v2) | Lightweight, no external API, runs locally |
| Vector Store | ChromaDB (embedded) | Zero infra overhead, single-file, hackathon-ready |
| AMD Runtime | ROCm on AMD MI300X | GPU-accelerated LLM + embedding inference |

---

## What We Built During the Hackathon

- `synthetic_apps.json` — 10 enterprise application records with full metadata (tech stack, age, CVE count, dependencies, business criticality, monthly cost)
- `knowledge_base/` — 15 curated modernization pattern documents covering all 6R decisions
- `ingest_kb.py` — ingests the knowledge base into ChromaDB with sentence-transformer embeddings
- `crew.py` — 3-agent CrewAI pipeline (Assessment → 6R Decision with RAG → Explanation)
- `main.py` — FastAPI endpoint: `POST /analyze` runs the crew, returns structured JSON report
- `app.py` — Streamlit dashboard: portfolio table, risk scores, 6R badges, retrieved patterns, explanations

**What we did NOT build (deliberately out of scope):**
- Dependency blast-radius analysis
- Wave planning (sequenced modernization order)
- Production database (PostgreSQL)
- Auth, user accounts, persistence

This split is intentional. **One flow, end to end, working and demonstrable** beats a shallow version of everything.

---

## The AMD Connection

Every time ModernizeIQ analyzes an application, two GPU workloads fire on the AMD MI300X:

1. **Embedding inference** — the app's metadata is embedded and compared against the knowledge base to retrieve the most relevant modernization patterns (sentence-transformers via ROCm)
2. **LLM inference** — Llama 3.1 8B reasons over the app's data + retrieved patterns to produce a scored, grounded recommendation (Ollama via ROCm)

Run this across a real enterprise portfolio — 500+ applications, analyzed continuously as systems evolve — and you have exactly the kind of mixed inference workload AMD hardware is built to serve: high-throughput, repeatable, parallelizable.

---

## Scope

### Built properly (in scope)
- 5 synthetic apps with full metadata
- 15-pattern knowledge base embedded into ChromaDB
- 3-agent CrewAI pipeline with RAG on the 6R agent
- FastAPI `/analyze` endpoint
- Streamlit dashboard: scores, 6R decisions, retrieved patterns, explanations
- Clean 3-minute demo end-to-end

### Explicitly out of scope (and that's fine)
- Dependency analysis and wave planning (roadmap item)
- Production database
- Large knowledge base (ours is curated and small — enough to prove the pattern)
- Any real enterprise integrations (Jira, ServiceNow, CMDB)

---

## Data

### Synthetic Applications (`synthetic_apps.json`)

5 apps designed to exercise all major 6R decisions:

| App | Stack | Age | CVEs | Monthly Cost | Expected 6R |
|-----|-------|-----|------|-------------|-------------|
| BillingCore | COBOL / z/OS | 22 yrs | 18 | $42,000 | Retire |
| CustomerAPI | Java 11 / Spring Boot | 3 yrs | 2 | $3,200 | Retain |
| ReportingLegacy | VB6 / Windows Server 2003 | 19 yrs | 31 | $18,500 | Replace |
| PaymentsGateway | Java 8 / Tomcat | 7 yrs | 9 | $8,100 | Replatform |
| InventoryService | .NET Framework 4.5 / IIS | 11 yrs | 14 | $11,200 | Refactor |

### Knowledge Base (`knowledge_base/`)

15 markdown documents covering:
- 6 pattern docs (one per 6R decision — conditions, indicators, risks, examples)
- 3 anti-pattern docs (common mistakes: rehosting something that should retire, refactoring low-value apps, retaining insecure legacy)
- 3 gotcha docs (hidden dependency traps, compliance deferrals, vendor lock-in considerations)
- 3 decision rationale docs (how to reason over ambiguous cases)

---

## How to Run

### Prerequisites
- Python 3.11+
- AMD Developer Cloud account with MI300X instance
- Ollama installed with ROCm support
- `ollama pull llama3.1:8b`

### Setup
```bash
git clone <repo>
cd modernizeiq
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
# requirements: crewai, fastapi, uvicorn, chromadb, sentence-transformers, streamlit, requests
```

### Ingest knowledge base (run once)
```bash
python ingest_kb.py
# Embeds all 15 knowledge base documents into ChromaDB
```

### Start the API
```bash
uvicorn main:app --reload
# API live at http://localhost:8000
```

### Start the dashboard
```bash
streamlit run app.py
# Dashboard at http://localhost:8501
```

### Run analysis
```bash
curl -X POST http://localhost:8000/analyze
# Returns: 5-app portfolio with scores, 6R decisions, retrieved patterns, explanations
```

---

## Demo Script (3 minutes)

**0:00 — The problem (30s)**
"Every big company runs on aging software. Deciding what to modernize — and in what order — takes consultants months and costs millions. The output is a static report that's stale the day it lands."

**0:30 — The solution (40s)**
"ModernizeIQ does that analysis in minutes. Three AI agents: one scores risk, one decides what to do with the app, one explains why. The decision agent doesn't guess — it retrieves real modernization patterns from a knowledge base first, so every recommendation is grounded in known practice. And every recommendation shows its evidence."

**1:10 — Live demo (80s)**
Open the dashboard. Click "Analyze Portfolio."
- Point to BillingCore: age 22 years, 18 CVEs, $42K/month → risk score 91 → **Retire** → show the retrieved legacy-retirement pattern that drove it
- Point to CustomerAPI: 3 years old, 2 CVEs → risk score 12 → **Retain** → show the "recently modernized" pattern
- Show the explanation paragraph — plain English, cites both the data and the retrieved pattern

**2:30 — AMD close (30s)**
"Every analysis runs two GPU workloads on the AMD MI300X — embedding inference for retrieval, LLM inference for reasoning. Scale this to a 500-app enterprise portfolio running continuously and you have a serious, mixed AI workload — exactly what AMD hardware is built for."

---

## Roadmap (what this becomes after the hackathon)

We know it's bigger than 5 days. Here's what's next:

- **Larger knowledge base** built from public AWS/Azure/GCP migration playbooks
- **Dependency blast-radius analysis** — which apps break if you touch this one?
- **Wave planning** — modernize apps in the right order, respecting dependencies
- **PostgreSQL + pgvector** for production-scale data and embeddings
- **Evaluation harness** — 20 golden test scenarios that define correct agent behavior
- **Enterprise integrations** — Jira, ServiceNow, CMDB

---

## Team

| Person | Role | Owns |
|--------|------|------|
| **Rohith** | Dev | CrewAI agents, prompts, RAG wiring, FastAPI, demo |
| **Sumedh** | Dev — Data & Retrieval | Synthetic data, knowledge base, ChromaDB ingestion, retrieval function |
| **Mahesh** | Story & Demo | Slides, demo script, AMD framing, presentation delivery |

---

*ModernizeIQ — TCS × AMD AI Hackathon. Synthetic data only. No real customer data is used or stored.*
