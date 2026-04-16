# Architecture

## System Overview

```mermaid
graph TB
    subgraph Users["👤 Users"]
        P["Parent / Teacher / Student\n(Reporter)"]
        CW["School Facilities Manager\n(Caseworker)"]
        TL["DfE School Delivery Manager\n(Portfolio View)"]
    end

    subgraph Frontend["🖥️ Frontend — React 18 + Tailwind CSS (port 3000)"]
        PORTAL["Reporting Portal\nAirQualityIntake · UploadPortal"]
        QUEUE["Case Queue\nCaseQueue · CaseDetail"]
        DASH["Portfolio Dashboard\nRiskDashboard · SchoolsAirQuality"]
    end

    subgraph Backend["⚙️ Backend — FastAPI / Python 3.12 (port 8000)"]
        CASES["Cases API\n/cases · /cases/{id}"]
        AQ["Air Quality API\n/cases/air-quality"]
        SAQ["Sensor Dashboard API\n/air-quality/schools"]
        AI_RT["AI Route\n/ai/cases/{id}/summarise\n/ai/cases/{id}/ask/stream"]
        RISK["Risk Engine\nrisk.py"]
        RECS["Recommendations\nrecommendations.py"]
        SEED["Seed Data\nseed_data.py"]
    end

    subgraph AI["🤖 AI Layer"]
        CLAUDE["Anthropic Claude\nHaiku 4.5\n(live mode)"]
        MOCK["Deterministic Mock\n(no API key)"]
    end

    subgraph Data["🗄️ Data"]
        PG[("PostgreSQL 16\ncases · timeline\nnotes · policies\nworkflow_states")]
        SENSOR["mock_school_air_quality.json\n5 schools × 36 months\nSAMHE-compatible sensor data"]
        SEED_FILES["Seed Files\ncases.json\npolicy-extracts.json\nworkflow-states.json"]
    end

    P -->|"Submit case / upload evidence"| PORTAL
    CW -->|"View & manage cases"| QUEUE
    TL -->|"Portfolio & sensor trends"| DASH

    PORTAL -->|"REST API"| AQ
    QUEUE -->|"REST API"| CASES
    QUEUE -->|"SSE stream"| AI_RT
    DASH -->|"REST API"| CASES
    DASH -->|"REST API"| SAQ

    CASES --> RISK
    CASES --> RECS
    AI_RT -->|"ANTHROPIC_API_KEY set"| CLAUDE
    AI_RT -->|"no key"| MOCK

    CASES <-->|"SQLAlchemy ORM"| PG
    AQ <-->|"SQLAlchemy ORM"| PG
    SAQ -->|"in-memory loader"| SENSOR
    SEED -->|"on startup"| SEED_FILES
    SEED -->|"populates"| PG
```

---

## Request Flow: Case Submission

```mermaid
sequenceDiagram
    actor Reporter as Parent / Teacher
    participant Portal as Reporting Portal
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    participant Risk as Risk Engine

    Reporter->>Portal: Fill in air quality concern form
    Portal->>API: POST /cases/air-quality
    API->>DB: Insert case + timeline event
    API->>Risk: Compute initial risk flag
    Risk-->>API: ok | reminder_due | escalation_due
    API-->>Portal: 201 Created { case_id, status }
    Portal-->>Reporter: Confirmation screen with case ID
```

---

## Request Flow: Caseworker AI Summary

```mermaid
sequenceDiagram
    actor CW as Caseworker
    participant UI as CaseDetail (React)
    participant API as FastAPI Backend
    participant DB as PostgreSQL
    participant AI as Claude / Mock

    CW->>UI: Open case view
    UI->>API: GET /cases/{id}
    API->>DB: Fetch case + timeline + workflow + policies
    DB-->>API: Case record
    API-->>UI: Case detail with risk flag + policy matches

    CW->>UI: Click "Summarise" or ask question
    UI->>API: POST /ai/cases/{id}/ask/stream
    API->>DB: Fetch full case context
    API->>AI: Prompt with case record + question
    AI-->>API: Streamed response (SSE)
    API-->>UI: Server-Sent Events stream
    UI-->>CW: Streamed answer in chat panel
```

---

## Data Model

```mermaid
erDiagram
    CASES {
        string id PK
        string case_type
        string status
        string severity_level
        bool is_urgent
        json submission_payload
        datetime created_at
        datetime updated_at
    }
    CASE_TIMELINE {
        int id PK
        string case_id FK
        string event_type
        string description
        datetime created_at
    }
    CASEWORKER_NOTES {
        int id PK
        string case_id FK
        string author
        text content
        datetime created_at
    }
    POLICIES {
        int id PK
        string policy_ref
        string case_type
        string title
        text extract
    }
    WORKFLOW_STATES {
        int id PK
        string case_type
        string state
        json required_actions
        json allowed_transitions
        int reminder_days
        int escalation_days
    }
    USERS {
        int id PK
        string username
        string team
        string role
    }

    CASES ||--o{ CASE_TIMELINE : "has"
    CASES ||--o{ CASEWORKER_NOTES : "has"
    CASES }o--|| WORKFLOW_STATES : "follows"
```

---

## Deployment

```mermaid
graph LR
    subgraph Docker Compose
        FE["frontend\nnode:20-alpine\n:3000"]
        BE["backend\npython:3.12-slim\n:8000"]
        DB["postgres:16\n:5432"]
    end

    FE -->|"VITE_API_URL\nHTTP/SSE"| BE
    BE -->|"DATABASE_URL"| DB
    BE -.->|"ANTHROPIC_API_KEY\n(optional)"| EXT["Anthropic API\n(external)"]
```

| Service | Image | Port | Key Env Vars |
|---|---|---|---|
| `frontend` | node:20-alpine | 3000 | `VITE_API_URL` |
| `backend` | python:3.12-slim | 8000 | `DATABASE_URL`, `ANTHROPIC_API_KEY` |
| `db` | postgres:16 | 5432 | `POSTGRES_DB`, `POSTGRES_USER`, `POSTGRES_PASSWORD` |
