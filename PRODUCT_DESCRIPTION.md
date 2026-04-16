---
marp: true
theme: default
paginate: true
style: |
  section {
    font-family: 'Segoe UI', Arial, sans-serif;
    background: #f0f7ff;
    color: #1e293b;
  }
  h1, h2 {
    color: #0f4c81;
  }
  h2 {
    border-bottom: 3px solid #38bdf8;
    padding-bottom: 0.3em;
  }
  section.lead {
    background: linear-gradient(135deg, #0f4c81 0%, #1e88e5 100%);
    color: white;
    text-align: center;
  }
  section.lead h1 {
    color: white;
    font-size: 2.2em;
  }
  section.lead p {
    color: #e0f2fe;
  }
  strong { color: #0f4c81; }
  section.small { font-size: 0.75em; }
---

<!-- _class: lead -->

# 🏫 School Air Quality Tracker

---

## 🏫 1 — School Air Quality Tracker

A prototype dashboard that amalgamates school-level air quality risks with crowd-sourced school-user reports, and guides proportionate action. It flags air quality risks to the people who need it.

---

## 🌫️ 2 — Problem

- Air pollution in schools has an adverse effect on pupil health, attendance and schooling. Effective interventions are often practical and affordable, but both interventions and current air quality levels are relatively unknown
- Parents and school staff lack a simple, localised view of air quality risks at each school, alongside an interpretation and advised interventions to summarise complex scientific data into actionable information
- Health workers and DfE need a way to aggregate data around school quality both from monitoring data and from reported symptoms or nuisance issues (odour, dust, mould).
- Existing systems are difficult to navigate, lack aggregation, and do not provide the opportunity to crowd source environmental information from parents and schools. 

---

## 👥 3 — Target users & use cases

- Key users: parents, school administrators, local public health officers, DfE Delivery Officers.
- Use cases:
  - Quickly check whether a school has high pollutant readings, either now (to understand current risks and mitigations needed) or historically (to support parent school choices and retrospective assessment of risk impacts).
  - Capture & display parent reports relating to air pollution
  - Triage and review system to identify air quality reports that need follow-up

---

## 💡 4 — Solution overview

- Public-facing dashboard showing 8 air quality issues at individual schools, detailed pollutant table, and parent reports (36 months data from 5 schools)
- Simplified Red-Amber-Green visualisation of pollutants including a certainty measure for quick risk assessment, alongside AI-recommended actions and guidelines
- Back-end report review system to track, AI-summarise, address and escalate issues. Reporters can check the status of their reports.

---

## ⭐ 5 — Key features

- Synthetic data modelled on realistic SAMHE programme data, CIBSE guidance, and WHO air quality guidelines.
- Per-school detail view: pollutant percentages, certainty badges, actions
- School-user reports: summary badges showing counts by type and a time-ordered list with reviewed status.
- Simple timeframe control (visible on individual school view) to investigate historical change.
- Report view for caseworkers to triage and action air quality reports, supported by AI summaries and identified related policies

---

## 🔒 6 — Data sources & privacy

- This prototpye is using synthetic data
- For any production system, we would need to ensure that no pupil-identifying data is shown to the public; sample reports would need to be anonymised and only describe symptoms/issues.


---

## ⚠️ 7 — Limitations & assumptions

- Prototype only. A production system would need to ensure end-users understand the risks and advice appropriately; this is not a substitute for clinical or environmental health advice.
- Indicators should be interpreted **as trends over time** and **within schools**, not as direct comparisons between schools.
- Metrics reflect **air-quality–sensitive outcomes**, not proof of causality.
- Where possible, indicators should be contextualised against local authority averages and seasonal effects.
- The purpose of these metrics is to **prompt awareness, investigation, and proportionate action**.
- Parent reports are illustrative; a production design needs verification, moderation, and audit trails.
- Code has been written by a variety of AI models. 

---

## 🗺️ 8 — Next steps / roadmap - 1

- Wire up real sensor feeds and a lightweight API for adding/reviewing parent reports.
- Add export and reporting for local public health teams.
- User research to establish understanding of the dashboard metrics
- Accessibility review; formalise privacy and retention policies.
- Enable schools and parents to enter their own data e.g. by hooking up local IoT sensors
- Aggregate data by Local Authority

---

## 🗺️ 8 - Next steps / roadmap - 2

- Embed AI support for air quality reporting to improve reported data quality
- Automated AI review of submitted photos and videos
- Enabling automated feedback for proportionate actions to take post-reporting
- AI-driven auto linking of relevant guidance
- AI filtering of malicious reports

---

## 🚀 9 — Extensions

- Add live data feeds
- Enable intervention reporting to track impacts on detected air quality issues
- Provide automated monitoring to flag peaks in automatically detected air quality issues and issues reported
- Enable school search. Add live data on schools from DfE.

---

## 🌦️ 10 — Edge Cases

- We have not modelled the impact of changing weather conditions. For example, a windy day may mitigate or worsen air quality issues depending on the direction.
- We need to introduce ventilation modelling. 
- We may have malicious reports. 
- AQ meters may be in a different location to the symptoms.



