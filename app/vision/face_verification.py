import cv2
import os
import uuid
from deepface import DeepFace

class FaceVerifier:
    def __init__(self, reference_image_path: str):
        self.reference_image = reference_image_path

    def verify(self, frame):
        """
        frame: OpenCV image (numpy array)
        """

        try:
            # 1️⃣ Create temp folder
            os.makedirs("data/temp", exist_ok=True)

            # 2️⃣ Save live frame as image
            temp_image_path = f"data/temp/{uuid.uuid4()}.jpg"
            cv2.imwrite(temp_image_path, frame)

            # 3️⃣ DeepFace verification (FILE vs FILE)
            result = DeepFace.verify(
                img1_path=temp_image_path,
                img2_path=self.reference_image,
                enforce_detection=False
            )

            # 4️⃣ Delete temp image
            os.remove(temp_image_path)

            return {
                "verified": bool(result.get("verified", False)),
                "confidence": round(1 - result.get("distance", 1), 2)
            }

        except Exception as e:
            return {
                "verified": False,
                "confidence": 0.0,
                "error": str(e)
            }
