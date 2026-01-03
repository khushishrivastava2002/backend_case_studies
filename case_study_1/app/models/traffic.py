from beanie import Document
from datetime import datetime
from pydantic import Field

class TrafficData(Document):
    timestamp: datetime = Field(default_factory=datetime.now)
    speed: float
    free_flow_speed: float
    jam_factor: float = 0.0
    location: str

    class Settings:
        name = "traffic_data"
