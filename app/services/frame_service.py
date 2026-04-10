def process_frame(session, face_count):
    session["total_frames"] += 1

    if face_count == 1:
        session["face_visible_frames"] += 1
    elif face_count == 0:
        session["violations"].append("NO_FACE")
    else:
        session["violations"].append("MULTIPLE_FACES")
