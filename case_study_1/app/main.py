from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.database import init_db
from app.routers import ingestion, analytics, alerts

import asyncio
from app.services.ingestion import process_traffic_data

async def run_scheduler():
    """
    Background task to run ingestion every 5 minutes.
    For demo purposes, we can set this to 10 seconds.
    """
    while True:
        try:
            print("Running scheduled ingestion...")
            await process_traffic_data()
        except Exception as e:
            print(f"Error in scheduler: {e}")
        
        # Wait for 5 minutes (300 seconds)
        # For testing/demo, let's keep it 60 seconds
        await asyncio.sleep(60)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    await init_db()
    print("Database initialized.")
    
    # Start the background scheduler
    asyncio.create_task(run_scheduler())
    
    yield
    # Shutdown
    print("Shutting down...")

app = FastAPI(
    title="Traffic Event & Analytics Service",
    description="Case Study 1: Traffic monitoring and event detection backend.",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(ingestion.router)
app.include_router(analytics.router)
app.include_router(alerts.router)

@app.get("/")
async def root():
    return {"message": "Traffic Analytics Service is running. Visit /docs for API documentation."}
