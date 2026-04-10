import cv2
import numpy as np
from mediapipe import solutions as mp_solutions

# -------------------------------
# MediaPipe Face Mesh
# -------------------------------
face_mesh = mp_solutions.face_mesh.FaceMesh(
    static_image_mode=False,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
)

# Landmark indexes
MOUTH_TOP = 13
MOUTH_BOTTOM = 14
LEFT_EYE = 33
RIGHT_EYE = 263
NOSE_TIP = 1


def analyze_face_behavior(frame):
    """
    Returns:
    {
        head_direction: LEFT / RIGHT / CENTER
        mouth_open: bool
        violations: []
    }
    """

    h, w, _ = frame.shape
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb)

    behavior = {
        "head_direction": "CENTER",
        "mouth_open": False,
        "violations": []
    }

    if not results.multi_face_landmarks:
        return behavior

    landmarks = results.multi_face_landmarks[0].landmark

    # -------------------------------
    # HEAD DIRECTION (simple logic)
    # -------------------------------
    nose_x = landmarks[NOSE_TIP].x * w

    if nose_x < w * 0.4:
        behavior["head_direction"] = "LEFT"
        behavior["violations"].append("LOOKING_AWAY")

    elif nose_x > w * 0.6:
        behavior["head_direction"] = "RIGHT"
        behavior["violations"].append("LOOKING_AWAY")

    # -------------------------------
    # MOUTH OPEN DETECTION
    # -------------------------------
    mouth_gap = abs(
        landmarks[MOUTH_TOP].y - landmarks[MOUTH_BOTTOM].y
    )

    if mouth_gap > 0.03:
        behavior["mouth_open"] = True
        behavior["violations"].append("TALKING")

    return behavior
