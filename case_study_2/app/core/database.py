from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from app.models import VehicleCountSession
from app.core.config import settings

async def init_db():
    client = AsyncIOMotorClient(settings.MONGODB_URI)
    await init_beanie(database=client[settings.DB_NAME], document_models=[VehicleCountSession])
