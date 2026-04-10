import cv2
import numpy as np


class MouthMovementDetector:
    """
    Detects mouth movement using pixel difference over time.
    """

    def __init__(self, threshold=15):
        self.prev_mouth_roi = None
        self.threshold = threshold

    def detect(self, frame, landmarks):
        """
        Returns:
            talking (bool)
        """
        if landmarks is None:
            return False

        x, y, w, h = landmarks["face_box"]

        # Approximate mouth region
        mouth_x = x + int(w * 0.3)
        mouth_y = y + int(h * 0.65)
        mouth_w = int(w * 0.4)
        mouth_h = int(h * 0.25)

        mouth_roi = frame[mouth_y:mouth_y + mouth_h, mouth_x:mouth_x + mouth_w]

        if mouth_roi.size == 0:
            return False

        gray = cv2.cvtColor(mouth_roi, cv2.COLOR_BGR2GRAY)
        gray = cv2.GaussianBlur(gray, (5, 5), 0)

        talking = False

        if self.prev_mouth_roi is not None:
            diff = cv2.absdiff(self.prev_mouth_roi, gray)
            mean_diff = np.mean(diff)

            if mean_diff > self.threshold:
                talking = True

        self.prev_mouth_roi = gray
        return talking
