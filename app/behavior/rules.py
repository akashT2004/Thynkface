import time
from collections import defaultdict


class BehaviorRulesEngine:
    """
    Rule-based behavior and anomaly detection.
    """

    def __init__(self):
        self.last_face_seen_time = time.time()
        self.look_away_counter = 0
        self.talking_counter = 0

        self.violations = set()

        # Thresholds (can be tuned)
        self.max_no_face_seconds = 3
        self.look_away_limit = 5
        self.talking_limit = 5

    def evaluate(self, frame_data):
        """
        Evaluate behavior rules per frame.

        Args:
            frame_data (dict): Output from websocket frame processing

        Returns:
            list: current violations
        """
        current_time = time.time()

        face_count = frame_data.get("face_count", 0)
        looking = frame_data.get("looking", "UNKNOWN")
        talking = frame_data.get("talking", False)

        # -------------------------------
        # NO FACE
        # -------------------------------
        if face_count == 0:
            if current_time - self.last_face_seen_time > self.max_no_face_seconds:
                self.violations.add("NO_FACE")
        else:
            self.last_face_seen_time = current_time
            self.violations.discard("NO_FACE")

        # -------------------------------
        # MULTIPLE FACES
        # -------------------------------
        if face_count > 1:
            self.violations.add("MULTIPLE_FACES")
        else:
            self.violations.discard("MULTIPLE_FACES")

        # -------------------------------
        # LOOKING AWAY
        # -------------------------------
        if looking in ["LEFT", "RIGHT", "UP", "DOWN"]:
            self.look_away_counter += 1
        else:
            self.look_away_counter = 0

        if self.look_away_counter >= self.look_away_limit:
            self.violations.add("LOOKING_AWAY")
        else:
            self.violations.discard("LOOKING_AWAY")

        # -------------------------------
        # TALKING
        # -------------------------------
        if talking:
            self.talking_counter += 1
        else:
            self.talking_counter = 0

        if self.talking_counter >= self.talking_limit:
            self.violations.add("TALKING")
        else:
            self.violations.discard("TALKING")

        return list(self.violations)
