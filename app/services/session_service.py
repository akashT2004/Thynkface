import uuid
import time

# -------------------------------
# In-memory session store
# -------------------------------
SESSIONS = {}

# Thresholds (seconds)
LOOKING_AWAY_TIME = 8
TALKING_TIME = 20
MULTIPLE_FACE_TIME = 10
WARNING_LIMIT = 3
WARNING_COOLDOWN = 20  # seconds between warnings


# -------------------------------
# START SESSION
# -------------------------------
def start_session():
    session_id = str(uuid.uuid4())

    SESSIONS[session_id] = {
        "start_time": time.time(),
        "total_frames": 0,
        "face_visible_frames": 0,

        # warnings
        "warning_count": 0,
        "last_warning_time": 0,
        "closed": False,

        # accumulated time
        "acc_time": {
            "LOOKING_AWAY": 0,
            "TALKING": 0
        },

        # continuous tracking
        "multiple_face_start": None,

        "violations": []
    }

    print("🆕 Session created:", session_id)
    return session_id


# -------------------------------
# GET SESSION
# -------------------------------
def get_session(session_id: str):
    return SESSIONS.get(session_id)


# -------------------------------
# INTERNAL WARNING CHECK
# -------------------------------
def _raise_warning(session, violation):
    now = time.time()

    # cooldown
    if now - session["last_warning_time"] < WARNING_COOLDOWN:
        return

    session["warning_count"] += 1
    session["last_warning_time"] = now
    session["violations"].append(violation)

    print(f"⚠️ Warning {session['warning_count']} → {violation}")

    if session["warning_count"] >= WARNING_LIMIT:
        session["closed"] = True
        print("🚨 SESSION AUTO CLOSED")


# -------------------------------
# UPDATE SESSION (PER FRAME)
# -------------------------------
def update_session(
    session_id: str,
    face_detected: bool,
    face_count: int,
    head_direction: str,
    mouth_open: bool
):
    session = SESSIONS.get(session_id)
    if not session or session["closed"]:
        return

    now = time.time()
    session["total_frames"] += 1

    if face_detected and face_count == 1:
        session["face_visible_frames"] += 1

    # -----------------------
    # MULTIPLE FACES (CONTINUOUS)
    # -----------------------
    if face_count > 1:
        if session["multiple_face_start"] is None:
            session["multiple_face_start"] = now
        elif now - session["multiple_face_start"] >= MULTIPLE_FACE_TIME:
            _raise_warning(session, "MULTIPLE_FACES")
            session["multiple_face_start"] = None
    else:
        session["multiple_face_start"] = None

    # -----------------------
    # LOOKING AWAY
    # -----------------------
    if head_direction in ["LEFT", "RIGHT", "DOWN"]:
        session["acc_time"]["LOOKING_AWAY"] += 1
        if session["acc_time"]["LOOKING_AWAY"] >= LOOKING_AWAY_TIME:
            _raise_warning(session, "LOOKING_AWAY")
            session["acc_time"]["LOOKING_AWAY"] = 0
    else:
        session["acc_time"]["LOOKING_AWAY"] = 0

    # -----------------------
    # TALKING (SAFE FOR DOUBTS)
    # -----------------------
    if mouth_open and head_direction != "CENTER":
        session["acc_time"]["TALKING"] += 1
        if session["acc_time"]["TALKING"] >= TALKING_TIME:
            _raise_warning(session, "TALKING")
            session["acc_time"]["TALKING"] = 0
    else:
        session["acc_time"]["TALKING"] = 0


# -------------------------------
# END SESSION
# -------------------------------
def end_session(session_id: str):
    return SESSIONS.pop(session_id, None)
