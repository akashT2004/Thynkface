# ThynkFace – Real-Time Face & Behavior Analysis

ThynkFace is a powerful, real-time facial monitoring and behavior analysis system. It leverages cutting-edge computer vision models to provide insights into face detection, head orientation, mouth status, and identity verification via a seamless WebSocket-based architecture.

## 🚀 Key Features

- **Real-Time Video Processing**: Stream camera frames via WebSockets for low-latency analysis.
- **Advanced Face Detection**: Uses high-performance **YuNet (ONNX)** for fast and accurate face detection.
- **Behavior Analysis**: Monitors head direction (Left, Right, Center) and mouth status (Open/Closed) using **MediaPipe Face Mesh**.
- **Face Verification**: Verifies identity against a reference image using **DeepFace**.
- **Violation Monitoring**: Tracks suspicious behaviors like looking away, talking, or multiple faces in view.
- **Session Management**: Automated session tracking with warning counts and auto-closure logic.

---

## 🛠 Tech Stack

- **Backend**: Python, FastAPI, Uvicorn (WebSocket support)
- **Computer Vision**: OpenCV (YuNet), MediaPipe, DeepFace, TensorFlow
- **Frontend**: Vanilla HTML5, CSS3, JavaScript (WebSocket integration)
- **Utilities**: Loguru (Logging), Pydantic (Data validation)

---

## 📂 Project Structure

```bash
thynkface/
├── app/
│   ├── api/            # REST API endpoints (Session management)
│   ├── behavior/       # (Core logic for behavior patterns)
│   ├── services/       # Business logic (Session store, warning system)
│   ├── vision/         # AI Logic
│   │   ├── models/     # ONNX models (YuNet)
│   │   ├── face_behavior.py    # MediaPipe Face Mesh logic
│   │   ├── face_detection.py   # YuNet detection logic
│   │   └── face_verification.py # DeepFace verification logic
│   ├── main.py         # App entry point & FastAPI setup
│   └── websocket.py    # WebSocket handler for live streaming
├── data/
│   ├── reference_faces/# Target images for face verification
│   └── temp/           # Temporary frame storage for DeepFace
├── frontend/
│   └── index.html      # Demo dashboard
├── requirements.txt    # Project dependencies
└── test_app.py         # Basic integration tests
```

---

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd thynkface
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
   > [!NOTE]
   > If `mediapipe` is not in your `requirements.txt`, install it manually: `pip install mediapipe`

---

## 🖥 Usage

### 1. Start the Backend
Run the FastAPI server using Uvicorn:
```bash
uvicorn app.main:app --reload
```
The backend will be available at `http://127.0.0.1:8000`.

### 2. Launch the Frontend
Simply open `frontend/index.html` in any modern web browser. 
- It will automatically request camera access.
- It will start a new session and begin real-time analysis.
- View the JSON output for live detections and violations.

---

## 🚦 Monitoring Logic (Violations)

ThynkFace tracks specific behaviors to ensure monitoring integrity:

- **LOOKING_AWAY**: Triggered if the head is turned left or right for more than 8 seconds.
- **TALKING**: Triggered if the mouth is open while looking away for more than 20 seconds.
- **MULTIPLE_FACES**: Triggered if more than one face is detected for more than 10 seconds.
- **Verified**: Displays a `verified` status and `confidence` score based on the reference image in `data/reference_faces/`.

**Session Termination**: If a user accumulates **3 warnings**, the session is automatically closed for security.

---

## 📄 License

This project is licensed under the MIT License.
