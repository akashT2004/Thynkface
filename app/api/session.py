from fastapi import APIRouter
from app.services.session_service import start_session, end_session

router = APIRouter()

# -------------------------------
# START SESSION
# -------------------------------
@router.post("/session/start")
def start_session_api():
    session_id = start_session()
    return {"session_id": session_id}


# -------------------------------
# END SESSION + FINAL REPORT
# -------------------------------
@router.post("/session/end")
def end_session_api(session_id: str):
    session = end_session(session_id)

    if not session:
        return {"error": "Invalid session"}

    total_frames = session.get("total_frames", 0)
    face_visible_frames = session.get("face_visible_frames", 0)

    # -----------------------
    # CLEAN VIOLATIONS
    # -----------------------
    # Remove duplicates + remove NONE
    raw_violations = session.get("violations", [])
    violations = list(set(v for v in raw_violations if v != "NONE"))

    # -----------------------
    # ATTENTION SCORE
    # -----------------------
    attention_score = (
        (face_visible_frames / total_frames) * 100
        if total_frames > 0 else 0
    )

    # -----------------------
    # FINAL REMARKS LOGIC
    # -----------------------
    if attention_score >= 85 and not violations:
        remarks = "Normal behavior"
    elif attention_score >= 70:
        remarks = "Attention dropped occasionally"
    else:
        remarks = "Attention dropped multiple times"

    return {
        "attention_score": round(attention_score, 2),
        "violations": violations,
        "remarks": remarks
    }
