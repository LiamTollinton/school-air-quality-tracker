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
data/
  mock_school_air_quality.json  — 5 UK schools × 36 months of SAMHE-style sensor data
  DATA_SPEC.md                  — Field definitions and RAG thresholds (CIBSE/WHO/UK NAQS)
CASE_SPECIFICATION.md           — Field spec for crowdsourced case reports
PERSONAS.md                     — User personas: reporters, school admin, DfE delivery managers
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
