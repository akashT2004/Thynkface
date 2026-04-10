import time


class AttentionTracker:
    def __init__(self):
        self.session_start = time.time()
        self.face_visible_frames = 0
        self.total_frames = 0

    def update(self, face_count):
        self.total_frames += 1

        if face_count == 1:
            self.face_visible_frames += 1

    def score(self):
        if self.total_frames == 0:
            return 0.0

        return round(
            (self.face_visible_frames / self.total_frames) * 100,
            2
        )
