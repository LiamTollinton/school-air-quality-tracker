"""AI layer for the caseworker assistant.

Two entry points: `summarise_case` and `ask_about_case_stream`.

Both support a mock mode (used when ANTHROPIC_API_KEY is unset). The mock
path produces deterministic, template-based output grounded in the case
data, so the demo still works without a model.
"""
import json
import os
from typing import AsyncGenerator, Iterable, List, Optional

MODEL = "claude-haiku-4-5-20251001"


def _has_key() -> bool:
    return bool(os.getenv("ANTHROPIC_API_KEY"))


def _client():
    import anthropic
    return anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))


SYSTEM = """You are an assistant for UK government caseworkers working on one of three case types:
benefit_review, licence_application, or compliance_check. You help caseworkers orient quickly on
a new case by surfacing what is known, what is missing, and what policy applies.

Be factual. Only use information in the provided case record. Never invent facts about the applicant,
timelines, or policy. If information is missing, say so."""


def _build_context(case, timeline, caseworker_notes, current_state, policies, risk: dict) -> str:
    lines = [
        f"## Case {case.case_id} — {case.case_type}",
        f"- Applicant: {case.applicant_name} ({case.applicant_reference or 'no ref'})",
        f"- Assigned to: {case.assigned_to or 'unassigned'}",
        f"- Status: {case.status}",
        f"- Created: {case.created_date} | Last updated: {case.last_updated}",
        f"- Risk flag: {risk['level']} — {risk['reason']}",
        "",
        "## Case notes",
        case.case_notes or "(none)",
        "",
        "## Timeline",
    ]
    for ev in timeline:
        lines.append(f"- {ev.date} · {ev.event}: {ev.note or ''}")

    if caseworker_notes:
        lines.append("")
        lines.append("## Caseworker notes")
        for n in caseworker_notes:
            lines.append(f"- [{n.created_at:%Y-%m-%d}] {n.author}: {n.content}")

    if current_state:
        lines.append("")
        lines.append(f"## Current workflow state: {current_state.label}")
        if current_state.description:
            lines.append(current_state.description)
        if current_state.required_actions:
            lines.append("Required actions:")
            for a in current_state.required_actions:
                lines.append(f"  - {a}")

    if policies:
        lines.append("")
        lines.append("## Applicable policy extracts")
        for p in policies:
            lines.append(f"- {p.policy_id} — {p.title}: {p.body}")

    return "\n".join(lines)


# ---- Summarise ----

def _mock_summary(case, timeline, current_state, risk) -> dict:
    last_event = timeline[-1] if timeline else None
    actions = (current_state.required_actions if current_state else []) or []
    next_action = actions[0] if actions else "Review case notes and decide next step."

    key_points = []
    if case.case_notes:
        first = case.case_notes.split(". ")[0].strip().rstrip(".")
        key_points.append(first + ".")
    if last_event:
        key_points.append(f"Most recent event on {last_event.date}: {last_event.event.replace('_', ' ')}.")
    if risk["level"] != "ok":
        key_points.append(risk["reason"])

    summary = (
        f"{case.applicant_name} — {case.case_type.replace('_', ' ')} currently {case.status.replace('_', ' ')}. "
        f"Created {case.created_date}, last updated {case.last_updated}. "
        f"{risk['reason']}"
    )
    return {
        "summary": summary,
        "key_points": key_points or ["No notes recorded yet."],
        "next_action": next_action,
        "mocked": True,
    }


def summarise_case(case, timeline, caseworker_notes, current_state, policies, risk: dict) -> dict:
    if not _has_key():
        return _mock_summary(case, timeline, current_state, risk)

    ctx = _build_context(case, timeline, caseworker_notes, current_state, policies, risk)
    resp = _client().messages.create(
        model=MODEL,
        max_tokens=500,
        system=SYSTEM + "\n\nProduce a briefing for the caseworker. Respond ONLY in JSON with fields: "
                       '{"summary": "3-sentence overview", "key_points": ["...", "..."], "next_action": "single concrete action"}',
        messages=[{"role": "user", "content": f"Brief me on this case:\n\n{ctx}"}],
    )
    text = resp.content[0].text
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        start, end = text.find("{"), text.rfind("}") + 1
        data = json.loads(text[start:end]) if start != -1 and end > start else {
            "summary": text, "key_points": [], "next_action": ""
        }
    data["mocked"] = False
    return data


# ---- Ask (streaming) ----

async def _mock_ask_stream(case, question: str, risk: dict, current_state) -> AsyncGenerator[str, None]:
    reply = (
        f"[Mock response — no ANTHROPIC_API_KEY set]\n\n"
        f"Based on case {case.case_id}: status is {case.status.replace('_', ' ')}, "
        f"risk is {risk['level']}. {risk['reason']}\n\n"
        f"Your question was: \"{question}\"\n\n"
    )
    if current_state and current_state.required_actions:
        reply += "Required actions at this stage:\n"
        for a in current_state.required_actions:
            reply += f"- {a}\n"
    # yield in small chunks to simulate streaming
    for i in range(0, len(reply), 40):
        yield reply[i:i + 40]


async def ask_about_case_stream(
    case, timeline, caseworker_notes, current_state, policies, risk: dict, question: str
) -> AsyncGenerator[str, None]:
    if not _has_key():
        async for chunk in _mock_ask_stream(case, question, risk, current_state):
            yield chunk
        return

    ctx = _build_context(case, timeline, caseworker_notes, current_state, policies, risk)
    with _client().messages.stream(
        model=MODEL,
        max_tokens=600,
        system=SYSTEM + "\nAnswer using ONLY the case record and policy extracts provided. "
                       "Cite policy IDs (e.g. POL-BR-003) where relevant.",
        messages=[{"role": "user", "content": f"Case record:\n\n{ctx}\n\nQuestion: {question}"}],
    ) as stream:
        for text in stream.text_stream:
            yield text
