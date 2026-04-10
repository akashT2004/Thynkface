import cv2

# Haar cascade for face detection
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)


class FaceLandmarkDetector:
    """
    Lightweight landmark approximation using face bounding box.
    This replaces MediaPipe for stability on Windows.
    """

    def get_landmarks(self, frame):
        """
        Approximate landmarks from face bounding box.

        Returns:
            dict or None
        """
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=5
        )

        if len(faces) == 0:
            return None

        # Take the first detected face
        (x, y, w, h) = faces[0]

        # Approximate regions
        landmarks = {
            "face_box": (x, y, w, h),
            "face_center": (x + w // 2, y + h // 2),
            "left_eye": (x + int(w * 0.3), y + int(h * 0.4)),
            "right_eye": (x + int(w * 0.7), y + int(h * 0.4)),
            "mouth": (x + w // 2, y + int(h * 0.75))
        }

        return landmarks
