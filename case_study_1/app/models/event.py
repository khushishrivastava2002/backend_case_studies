from beanie import Document
from datetime import datetime
from typing import Optional
from pydantic import Field

from enum import Enum

class EventStatus(str, Enum):
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"

class CongestionEvent(Document):
    event_type: str = "CONGESTION"
    start_time: datetime = Field(default_factory=datetime.now)
    end_time: Optional[datetime] = None
    status: EventStatus = EventStatus.ACTIVE
    location: str

    class Settings:
        name = "congestion_events"
