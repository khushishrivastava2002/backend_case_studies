from fastapi import APIRouter
from app.services.ingestion import process_traffic_data

router = APIRouter(prefix="/ingest", tags=["Ingestion"])

@router.post("/run")
async def run_ingestion():
    """
    Triggers the data ingestion and event detection process manually.
    """
    result = await process_traffic_data()
    return {"status": "success", "details": result}
