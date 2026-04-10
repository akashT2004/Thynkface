from fastapi import APIRouter, WebSocket, WebSocketDisconnect
import base64
import cv2
import numpy as np

from app.vision.face_detection import detect_faces
from app.vision.face_verification import FaceVerifier
from app.vision.face_behavior import analyze_face_behavior
from app.services.session_service import get_session, update_session

websocket_router = APIRouter()
verifier = FaceVerifier("data/reference_faces/A1.jpg")


@websocket_router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()

    session_id = websocket.query_params.get("session_id")
    session = get_session(session_id)

    if not session:
        await websocket.send_json({"error": "Invalid session"})
        await websocket.close()
        return

    print(f"🟢 WebSocket connected | {session_id}")

    try:
        while True:
            if session["closed"]:
                await websocket.send_json({
                    "session_closed": True,
                    "message": "Session closed due to warnings"
                })
                await websocket.close()
                break

            data = await websocket.receive_text()
            frame = cv2.imdecode(
                np.frombuffer(base64.b64decode(data), np.uint8),
                cv2.IMREAD_COLOR
            )

            if frame is None:
                continue

            face_info = detect_faces(frame)

            head_direction = "CENTER"
            mouth_open = False

            if face_info["face_count"] == 1:
                behavior = analyze_face_behavior(frame)
                head_direction = behavior["head_direction"]
                mouth_open = behavior["mouth_open"]

            update_session(
                session_id=session_id,
                face_detected=face_info["face_detected"],
                face_count=face_info["face_count"],
                head_direction=head_direction,
                mouth_open=mouth_open
            )

            response = {
                "face_detected": face_info["face_detected"],
                "face_count": face_info["face_count"],
                "head_direction": head_direction,
                "mouth_open": mouth_open,
                "warning_count": session["warning_count"],
                "violations": list(set(session["violations"]))
            }

            if face_info["face_count"] == 1:
                response.update(verifier.verify(frame))

            await websocket.send_json(response)

    except WebSocketDisconnect:
        print(f"🔴 WebSocket disconnected | {session_id}")
