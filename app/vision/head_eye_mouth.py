import mediapipe as mp
import cv2
import math

mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# Landmark indexes
LEFT_EYE = [33, 133]
RIGHT_EYE = [362, 263]
UPPER_LIP = 13
LOWER_LIP = 14
NOSE_TIP = 1


def analyze_head_eye_mouth(frame):
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = face_mesh.process(rgb)

    output = {
        "head_direction": "CENTER",
        "mouth_open": False
    }

    if not result.multi_face_landmarks:
        return output

    landmarks = result.multi_face_landmarks[0].landmark
    h, w, _ = frame.shape

    nose_x = landmarks[NOSE_TIP].x * w
    left_eye_x = landmarks[LEFT_EYE[0]].x * w
    right_eye_x = landmarks[RIGHT_EYE[0]].x * w

    # -------- HEAD DIRECTION --------
    if nose_x < left_eye_x:
        output["head_direction"] = "LEFT"
    elif nose_x > right_eye_x:
        output["head_direction"] = "RIGHT"
    else:
        output["head_direction"] = "CENTER"

    # -------- MOUTH OPEN --------
    lip_distance = abs(
        (landmarks[UPPER_LIP].y - landmarks[LOWER_LIP].y) * h
    )

    if lip_distance > 8:
        output["mouth_open"] = True

    return output
