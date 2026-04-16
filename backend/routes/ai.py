from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from models import get_db, Case, Policy, WorkflowState
from schemas import AISummaryOut
from ai_pipeline import summarise_case, ask_about_case_stream
from risk import compute_risk

router = APIRouter(prefix="/ai", tags=["ai"])


def _load(case_id: str, db: Session):
    case = db.query(Case).filter(Case.case_id == case_id).first()
    if not case:
        raise HTTPException(status_code=404, detail="Case not found")

    current = db.query(WorkflowState).filter(
        WorkflowState.case_type == case.case_type,
        WorkflowState.state == case.status,
    ).first()
    awaiting = db.query(WorkflowState).filter(
        WorkflowState.case_type == case.case_type,
        WorkflowState.state == "awaiting_evidence",
    ).first()
    policies = [
        p for p in db.query(Policy).all()
        if case.case_type in (p.applicable_case_types or [])
    ]
    risk = compute_risk(case, awaiting)
    return case, case.timeline, case.caseworker_notes, current, policies, risk


@router.post("/cases/{case_id}/summarise", response_model=AISummaryOut)
def ai_summarise(case_id: str, db: Session = Depends(get_db)):
    case, timeline, notes, current, policies, risk = _load(case_id, db)
    result = summarise_case(case, timeline, notes, current, policies, risk)
    case.ai_summary = result.get("summary", "")
    db.commit()
    return AISummaryOut(**result)


@router.get("/cases/{case_id}/ask/stream")
async def ai_ask_stream(case_id: str, question: str, db: Session = Depends(get_db)):
    case, timeline, notes, current, policies, risk = _load(case_id, db)

    async def event_gen():
        async for chunk in ask_about_case_stream(case, timeline, notes, current, policies, risk, question):
            # Preserve newlines by escaping; client unescapes.
            yield f"data: {chunk}\n\n"
        yield "data: [DONE]\n\n"

    return StreamingResponse(event_gen(), media_type="text/event-stream")
