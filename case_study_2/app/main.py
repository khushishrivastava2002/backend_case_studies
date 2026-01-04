from fastapi import FastAPI, BackgroundTasks
from app.core.database import init_db
from app.models import VehicleCountSession
from app.services.video_processor import VideoProcessor
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/start-processing")
async def start_processing(background_tasks: BackgroundTasks, video_url: str = "https://www.youtube.com/live/B0YjuKbVZ5w?si=Pgn-xB8PE9v_p9RO", duration_minutes: int = 3):
    session = VehicleCountSession()
    await session.save()
    
    processor = VideoProcessor(session.id, video_url, duration_minutes)
    background_tasks.add_task(processor.process)
    
    return {"session_id": str(session.id), "status": "Processing started"}

@app.get("/sessions")
async def get_sessions():
    sessions = await VehicleCountSession.find_all().to_list()
    return sessions

@app.get("/sessions/{session_id}")
async def get_session(session_id: str):
    session = await VehicleCountSession.get(session_id)
    return session
