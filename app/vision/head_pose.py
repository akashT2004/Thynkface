import cv2
import numpy as np

# Landmark indices (MediaPipe)
NOSE_TIP = 1
CHIN = 152
LEFT_EYE = 33
RIGHT_EYE = 263
LEFT_MOUTH = 61
RIGHT_MOUTH = 291

def estimate_head_pose(landmarks, frame_shape):
    """
    Estimate head pose direction.

    Returns:
        dict: head pose info
    """
    h, w = frame_shape[:2]

    image_points = np.array([
        (landmarks.landmark[NOSE_TIP].x * w,
         landmarks.landmark[NOSE_TIP].y * h),
        (landmarks.landmark[CHIN].x * w,
         landmarks.landmark[CHIN].y * h),
        (landmarks.landmark[LEFT_EYE].x * w,
         landmarks.landmark[LEFT_EYE].y * h),
        (landmarks.landmark[RIGHT_EYE].x * w,
         landmarks.landmark[RIGHT_EYE].y * h),
        (landmarks.landmark[LEFT_MOUTH].x * w,
         landmarks.landmark[LEFT_MOUTH].y * h),
        (landmarks.landmark[RIGHT_MOUTH].x * w,
         landmarks.landmark[RIGHT_MOUTH].y * h),
    ], dtype="double")

    model_points = np.array([
        (0.0, 0.0, 0.0),
        (0.0, -330.0, -65.0),
        (-225.0, 170.0, -135.0),
        (225.0, 170.0, -135.0),
        (-150.0, -150.0, -125.0),
        (150.0, -150.0, -125.0)
    ])

    focal_length = w
    center = (w / 2, h / 2)
    camera_matrix = np.array([
        [focal_length, 0, center[0]],
        [0, focal_length, center[1]],
        [0, 0, 1]
    ], dtype="double")

    dist_coeffs = np.zeros((4, 1))

    success, rotation_vector, _ = cv2.solvePnP(
        model_points,
        image_points,
        camera_matrix,
        dist_coeffs,
        flags=cv2.SOLVEPNP_ITERATIVE
    )

    if not success:
        return {"looking": "UNKNOWN"}

    rmat, _ = cv2.Rodrigues(rotation_vector)
    angles, _, _, _, _, _ = cv2.RQDecomp3x3(rmat)

    pitch, yaw, roll = angles

    looking = "CENTER"
    if yaw > 15:
        looking = "RIGHT"
    elif yaw < -15:
        looking = "LEFT"
    elif pitch > 15:
        looking = "DOWN"
    elif pitch < -15:
        looking = "UP"

    return {
        "looking": looking,
        "yaw": round(yaw, 2),
        "pitch": round(pitch, 2),
        "roll": round(roll, 2)
    }
