# Simple in-memory session store (demo purpose)

SESSION_STORE = {}

def create_session(session_id: str):
    SESSION_STORE[session_id] = {
        "events": []
    }

def record_event(session_id: str, event: dict):
    if session_id in SESSION_STORE:
        SESSION_STORE[session_id]["events"].append(event)

def get_session(session_id: str):
    return SESSION_STORE.get(session_id)

def end_session(session_id: str):
    return SESSION_STORE.pop(session_id, None)
