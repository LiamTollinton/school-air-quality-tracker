# School Air Quality Tracker

A platform for monitoring, reporting, and managing air quality concerns in UK schools — combining **crowdsourced case reports** from parents and staff with **administrative sensor data** from SAMHE-compatible monitors.

Built as a prototype for the **Version 1 AI Engineering Lab Hackathon, April 2026**.

## Problem

Poor air quality in school buildings — mould, inadequate ventilation, high CO₂, chemical smells — has a measurable impact on pupil health and learning outcomes. But there is no joined-up system for:
- parents and staff to report concerns and track what's being done
- school facilities managers to triage, assign, and resolve cases
- DfE School Delivery Managers to spot patterns across their portfolio and evidence funding needs

Information is scattered across email inboxes, maintenance logs, and sensor dashboards with no connection between them.

## Solution

## Architecture snapshot (read this first)

```
┌────────────────────┐       ┌──────────────────────┐       ┌─────────────────┐
│  React 18 + Vite   │──────▶│  FastAPI (Python)    │──────▶│  PostgreSQL 16  │
│  + Tailwind        │  REST │  - stateless         │ SQL   │  (SQLite in     │
│  (GOV.UK styling)  │  SSE  │  - SQLAlchemy 2      │       │   tests)        │
└────────────────────┘       └──────────┬───────────┘       └─────────────────┘
                                        │ 
                                        ▼
                             ┌──────────────────────┐
                             │  Claude Haiku 4.5    │
                             │  (+ mock fallback)   │
                             └──────────────────────┘

Three surfaces:

1. **Reporting portal** — parents, teachers, and students submit air quality concern cases with location, category, severity, health impacts, and photo evidence
2. **Caseworker view** — school facilities managers see all open cases with timeline, workflow status, required actions, and linked sensor readings for the same location
3. **Portfolio dashboard** — DfE Delivery Managers see cases aggregated across their school portfolio, with RAG-rated sensor trends and risk flags for schools approaching or breaching thresholds

An optional AI layer (Claude, or a deterministic mock) summarises cases and answers questions grounded in the case record and sensor data.

## Key Features

### Crowdsourced Case Management
- Community reporting of air quality issues by parents, teachers, and students
- Case lifecycle: `Open → Investigating → In Progress → Resolved`
- Evidence attachments (photos, medical reports, maintenance records)
- Automatic flagging when a location has prior reports

### Administrative Sensor Data
- SAMHE-compatible monthly readings: CO₂, PM2.5, PM10, NO₂, TVOC, temperature, humidity
- RAG-rated against CIBSE, WHO, and UK NAQS thresholds
- Seasonal trend analysis with school-in-session context
- Cross-referenced with crowdsourced cases from the same school

### DfE Portfolio View
- Aggregated case volumes by school, severity, and region
- Sensor trend summaries across portfolio
- Risk flagging for schools with persistent poor readings or unresolved escalated cases

## Quick Start

```bash
# Optional — without it, AI runs in mocked mode
export ANTHROPIC_API_KEY=sk-ant-your-key

docker compose up --build

# Frontend: http://localhost:3000
# API docs: http://localhost:8000/docs
```

## Stack

- **Backend:** FastAPI + PostgreSQL
- **Frontend:** React + Tailwind CSS (GOV.UK design language)
- **AI:** Claude API (Haiku 4.5) — optional, deterministic mock fallback
- **Infra:** Docker Compose

## Repository Structure

```
school-air-quality-tracker/
├── docker-compose.yml              — Orchestrates backend, frontend, and PostgreSQL
├── CLAUDE.md                       — AI agent context and project conventions
│
├── backend/                        — FastAPI application (Python 3.12)
│   ├── main.py                     — App entry point: CORS, lifespan, seed
│   ├── models.py                   — SQLAlchemy models (cases, timeline, notes, policies, users)
│   ├── schemas.py                  — Pydantic request/response schemas
│   ├── risk.py                     — Pure-Python risk flag computation
│   ├── recommendations.py          — Rules-based recommended actions
│   ├── school_air_quality.py       — In-memory loader for sensor data; RAG/threshold helpers
│   ├── ai_pipeline.py              — Claude + deterministic mock fallback
│   ├── seed_data.py                — Loads JSON seed files into the database
│   ├── requirements.txt
│   ├── requirements-dev.txt
│   ├── Dockerfile
│   ├── routes/
│   │   ├── cases.py                — CRUD, case detail, dashboard, workflow, policies
│   │   ├── ai.py                   — /ai/cases/{id}/summarise, /ai/cases/{id}/ask/stream
│   │   ├── air_quality.py          — POST /cases/air-quality (8-section specialist intake)
│   │   ├── school_air_quality.py   — GET /air-quality/schools + /{urn} (sensor dashboard)
│   │   └── upload.py               — Generic case submission endpoint
│   └── tests/
│       ├── conftest.py             — Pytest fixtures (in-memory SQLite DB)
│       ├── test_cases_routes.py
│       ├── test_air_quality.py
│       ├── test_school_air_quality.py
│       ├── test_risk.py
│       ├── test_ai_mock.py
│       ├── test_applicant.py
│       └── test_upload.py
│
├── frontend/                       — React 18 + Vite + Tailwind (GOV.UK design language)
│   ├── src/
│   │   ├── App.jsx                 — Layout, nav, user switcher, AI-mode badge
│   │   ├── api.js                  — Fetch wrapper / API base URL
│   │   └── components/
│   │       ├── CaseQueue.jsx       — Filterable case list with risk pills and severity chips
│   │       ├── CaseDetail.jsx      — Three-panel view: timeline | workflow | policy + AI chat
│   │       ├── RiskDashboard.jsx   — Team leader backlog, escalation flags, AQ portfolio view
│   │       ├── AirQualityIntake.jsx — 8-section specialist intake form
│   │       ├── SchoolsAirQuality.jsx — Parent-facing sensor dashboard (RAG/trend/sources)
│   │       ├── UploadPortal.jsx    — Generic case submission form
│   │       └── ApplicantPortal.jsx — Applicant-facing case tracking portal
│   ├── index.html
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── Dockerfile
│
├── data/                           — Seed and reference data (JSON + Markdown)
│   ├── cases.json                  — 20 synthetic cases (10 legacy + 10 air quality)
│   ├── policy-extracts.json        — 15 policy extracts (incl. POL-AQ-001..005)
│   ├── workflow-states.json        — State machine per case type with reminder/escalation days
│   ├── mock_school_air_quality.json — 5 UK schools × 36 months × 8 measures (SAMHE-style)
│   ├── DATA_SPEC.md                — Authoritative thresholds: CIBSE TM21/BB101, WHO AQG, UK NAQS
│   └── claims.json                 — Legacy claims seed data
│
└── docs/                           — Project documentation
    ├── ARCHITECTURE.md             — System design and decision log
    ├── CASE_SPECIFICATION.md       — Field spec for crowdsourced case reports
    ├── PERSONAS.md                 — User personas: reporters, school admin, DfE delivery managers
    ├── PRODUCT_DESCRIPTION.md      — Product vision and feature overview
    ├── problem_context.md          — Background and problem framing
    └── REBUILD_PLAYBOOK.md         — Phased prompts to rebuild the project from scratch
```

## Personas

| Persona | Role |
|---|---|
| Parent / Carer | Submits and tracks case reports |
| Teacher / Staff | Reports issues, adds evidence |
| School Facilities Manager | Triages, assigns, resolves cases |
| Headteacher / SLT | Portfolio overview for governance |
| DfE School Delivery Manager | Cross-school monitoring and funding evidence |

See [PERSONAS.md](PERSONAS.md) for full detail.
