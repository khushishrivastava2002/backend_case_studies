from fastapi import APIRouter
from app.models.traffic import TrafficData
from app.models.event import CongestionEvent
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

@router.get("/hourly-speeds")
async def get_hourly_speeds():
    """
    Returns average speed per hour for the current day.
    """
    # Simple aggregation pipeline
    pipeline = [
        {
            "$group": {
                "_id": {
                    "year": {"$year": "$timestamp"},
                    "month": {"$month": "$timestamp"},
                    "day": {"$dayOfMonth": "$timestamp"},
                    "hour": {"$hour": "$timestamp"}
                },
                "average_speed": {"$avg": "$speed"},
                "count": {"$sum": 1}
            }
        },
        {"$sort": {"_id.year": 1, "_id.month": 1, "_id.day": 1, "_id.hour": 1}}
    ]
    
    # Use Motor collection directly to avoid Beanie await error with aggregate
    collection = TrafficData.get_pymongo_collection()
    results = await collection.aggregate(pipeline).to_list(length=None)
    
    # Format for easier consumption
    formatted = []
    for r in results:
        dt_str = f"{r['_id']['year']}-{r['_id']['month']}-{r['_id']['day']} {r['_id']['hour']}:00"
        formatted.append({
            "hour": dt_str,
            "average_speed": round(r["average_speed"], 2),
            "sample_count": r["count"]
        })
        
    return formatted

@router.get("/summary")
async def get_summary():
    """
    Returns total congestion events and duration for today.
    """
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    
    events = await CongestionEvent.find(
        CongestionEvent.start_time >= today_start
    ).to_list()
    
    total_duration_minutes = 0
    for e in events:
        end = e.end_time if e.end_time else datetime.now()
        duration = (end - e.start_time).total_seconds() / 60
        total_duration_minutes += duration
        
    return {
        "total_events": len(events),
        "total_duration_minutes": round(total_duration_minutes, 2)
    }
