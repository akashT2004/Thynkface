def generate_report(session):
    total = session["total_frames"]
    visible = session["face_visible_frames"]

    attention = (visible / total) * 100 if total > 0 else 0

    return {
        "attention_score": round(attention, 2),
        "violations": list(set(session["violations"])),
        "remarks": "Attention dropped multiple times" if attention < 80 else "Good attention"
    }
