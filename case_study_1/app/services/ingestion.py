import random
from datetime import datetime
from app.models.traffic import TrafficData
from app.models.event import CongestionEvent, EventStatus

LOCATION = "Western Express Highway (Andheri-Bandra)"
FREE_FLOW_SPEED = 60.0

async def fetch_traffic_data() -> dict:
    """
    Simulates fetching data from HERE Traffic API.
    Returns a dictionary with speed, jam_factor, and timestamp.
    """
    # Mock logic: Generate realistic correlated data
    # High Speed = Low Jam Factor
    # Low Speed = High Jam Factor
    
    # 1. Generate a random "congestion level" (0.0 to 1.0)
    # 0.0 = Empty Road, 1.0 = Blocked
    congestion_level = random.random()
    
    # 2. Calculate Jam Factor (0 to 10)
    jam_factor = round(congestion_level * 10, 2)
    
    # 3. Calculate Speed based on Jam Factor
    # If Jam Factor is 10, Speed is near 0.
    # If Jam Factor is 0, Speed is near Free Flow (60).
    # Adding some randomness (+/- 5 km/h) to make it look real
    calculated_speed = FREE_FLOW_SPEED * (1 - congestion_level)
    noise = random.uniform(-5, 5)
    final_speed = max(0, min(FREE_FLOW_SPEED + 10, calculated_speed + noise))
    
    return {
        "speed": round(final_speed, 2),
        "free_flow_speed": FREE_FLOW_SPEED,
        "jam_factor": jam_factor,
        "location": LOCATION,
        "timestamp": datetime.now()
    }

async def process_traffic_data():
    """
    Orchestrates data ingestion and event detection.
    """
    # 1. Fetch Data
    data = await fetch_traffic_data()
    
    # 2. Store Data
    traffic_entry = TrafficData(**data)
    await traffic_entry.insert()
    
    # 3. Event Detection Logic
    # Check for existing active event
    active_event = await CongestionEvent.find_one(
        CongestionEvent.location == LOCATION,
        CongestionEvent.status == EventStatus.ACTIVE
    )
    
    jam_factor = data["jam_factor"]
    
    if active_event:
        # Check if congestion is cleared
        # Threshold: Jam Factor < 4.0 (approx > 36 km/h)
        if jam_factor < 4.0:
            active_event.end_time = datetime.now()
            active_event.status = EventStatus.RESOLVED
            await active_event.save()
            print(f"Event RESOLVED at {active_event.end_time} (JF: {jam_factor})")
    else:
        # Check if congestion started
        # Threshold: Jam Factor > 8.0 (approx < 12 km/h) - High Congestion
        if jam_factor > 8.0:
            new_event = CongestionEvent(
                location=LOCATION,
                status=EventStatus.ACTIVE,
                start_time=datetime.now()
            )
            await new_event.insert()
            print(f"Event STARTED at {new_event.start_time} (JF: {jam_factor})")

    return {
        "data": data,
        "event_status": "ACTIVE" if active_event or (jam_factor > 8.0) else "NORMAL"
    }
