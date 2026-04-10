import cv2
import numpy as np
import os

# -------------------------------
# Load YuNet Face Detector (ONNX)
# -------------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(
    BASE_DIR,
    "models",
    "face_detection_yunet_2023mar.onnx"
)

# Safety check (VERY IMPORTANT)
if not os.path.exists(MODEL_PATH):
    raise FileNotFoundError(f"YuNet model not found at: {MODEL_PATH}")

face_detector = cv2.FaceDetectorYN.create(
    MODEL_PATH,
    "",
    (320, 320),
    score_threshold=0.6,
    nms_threshold=0.3,
    top_k=5000
)

def detect_faces(frame):
    """
    Fast face detection using OpenCV YuNet (NO torch, NO mediapipe)
    """
    h, w = frame.shape[:2]

    # Update input size dynamically
    face_detector.setInputSize((w, h))

    _, faces = face_detector.detect(frame)

    face_count = 0
    if faces is not None:
        face_count = faces.shape[0]

    return {
        "face_detected": face_count > 0,
        "face_count": face_count
    }
