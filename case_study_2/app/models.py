from beanie import Document
from pydantic import Field
from datetime import datetime
from typing import Dict, Optional

class VehicleCountSession(Document):
    start_time: datetime = Field(default_factory=datetime.utcnow)
    end_time: Optional[datetime] = None
    duration_seconds: Optional[float] = None
    counts: Dict[str, int] = Field(default_factory=lambda: {"incoming": 0, "outgoing": 0})
    video_path: Optional[str] = None
    status: str = "PENDING"  # PENDING, PROCESSING, COMPLETED, FAILED

    class Settings:
        name = "vehicle_count_sessions"
