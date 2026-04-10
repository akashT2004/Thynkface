from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.session import router as session_router
from app.websocket import websocket_router

app = FastAPI(
    title="ThynkFace – Face & Behavior Analysis",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(session_router)
app.include_router(websocket_router)

@app.get("/")
def root():
    return {"message": "ThynkFace backend running"}
