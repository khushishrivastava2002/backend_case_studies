from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.core.config import get_settings
from app.models.traffic import TrafficData
from app.models.event import CongestionEvent

async def init_db():
    settings = get_settings()
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    
    await init_beanie(
        database=client[settings.DATABASE_NAME],
        document_models=[
            TrafficData,
            CongestionEvent
        ]
    )
