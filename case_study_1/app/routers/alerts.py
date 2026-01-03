from fastapi import APIRouter
from app.models.event import CongestionEvent, EventStatus
from typing import List

router = APIRouter(prefix="/alerts", tags=["Alerts"])

@router.get("/active", response_model=List[CongestionEvent])
async def get_active_alerts():
    """
    Returns all currently active congestion events.
    """
    return await CongestionEvent.find(CongestionEvent.status == EventStatus.ACTIVE).to_list()

@router.get("/history", response_model=List[CongestionEvent])
async def get_alert_history():
    """
    Returns history of all congestion events.
    """
    return await CongestionEvent.find_all().sort("-start_time").to_list()
