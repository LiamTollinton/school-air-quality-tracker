# School Air Quality Tracker — Product Description

---

## Slide 1 — Title

**School Air Quality Tracker **

A prototype dashboard that surfaces school-level air quality risks, crowd-sources parent reports, and guides proportionate action — bridging monitoring data and the people who need it.

---

## Slide 2 — Problem

- Air pollution in schools has an adverse effect on pupil health, attendance and schooling.
- Effective interventions are often practical and affordable, but both interventions and current air quality levels are relatively unknown
- Parents and school staff lack a simple, localised view of air quality risks at each school, alongside an interpretation and advised interventions to summarise complex scientific data into actionable information
- Health workers and DfE need a way to aggregate data around school quality both from monitoring data and from reported symptoms or nuisance issues (odour, dust, mould).
- Existing systems are difficult to navigate, lack aggregation, and do not provide the opportunity to crowd source environmental information from parents and schools. 

---

## Slide 3 — Target users & use cases

- Primary users: parents, school administrators, local public health officers.
- Use cases:
  - Quickly check whether a school has high pollutant readings, either now (to understand current risks and mitigations needed) or historically (to support school choice and retrospective assessment of risk impacts).
  - See recent parent reports by category and date.
  - Capture parent reports relating to air pollution and triage items that need follow-up.

---

## Slide 4 — Solution overview

- Single-page mock dashboard showing schools list, detailed pollutant table, and parent reports per school.
- RAG (Red/Amber/Green) visualisation for quick risk assessment.
- Parent reports grouped by type (Odor, Dust/Particles, Mould/Moisture, Chemical Smell, Poor Ventilation, Temperature Issues, Other) with counts and last-reported date.

---

## Slide 5 — Key features

- Syntheitc data modelled on realistic SAMHE programme data, CIBSE guidance, and WHO air quality guidelines.
- Per-school detail view: pollutant percentages, certainty badges, actions, and sources.
- Parent reports: summary badges showing counts by type and a time-ordered list with reviewed status.
- Simple timeframe control (visible on individual school view) to investigate historical change.

---

## Slide 6 — Data sources & privacy

- For any production system, we would need to ensure that no pupil-identifying data is shown to the public; sample reports need to be anonymised and only describe symptoms/issues.
- We are using synthetic data

---

## Slide 7 — Limitations & assumptions

- Prototype only. A production system would need to ensure end-users understand the risks and advice appropriately; this is not a substitute for clinical or environmental health advice.
- Indicators should be interpreted **as trends over time** and **within schools**, not as direct comparisons between schools.
- Metrics reflect **air-quality–sensitive outcomes**, not proof of causality.
- Where possible, indicators should be contextualised against local authority averages and seasonal effects.
- The purpose of these metrics is to **prompt awareness, investigation, and proportionate action**.
- Parent reports are illustrative; a production design needs verification, moderation, and audit trails.
- Code has been written by a variety of AI models. 

---

## Slide 8 — Next steps / roadmap

- Wire up real sensor feeds and a lightweight API for adding/reviewing parent reports.
- Add export and reporting for local public health teams.
- User research to establish understanding of the dashboard metrics
- Accessibility review; formalise privacy and retention policies.
- Enable schools and parents to enter their own data e.g. by hooking up local sensors

## Slide 9 - Extensions

- Add live data feeds
- Enable intervention reporting to track impacts on detected air quality issues
- Provide automated monitoring to flag peaks in automatically detected air quality issues and issues reported
- Enable school search. Add live data on schools from DfE.

## Slide 10 - Edge Cases

- We have not modelled the impact of changing weather conditions. For example, a windy day may mitigate or worsen air quality issues depending on the direction.
- We need to introduce ventilation modelling. 

---

