import requests
import time
import random

BASE_URL = "http://localhost:8000"

def run_ingestion():
    print("Triggering ingestion...")
    response = requests.post(f"{BASE_URL}/ingest/run")
    print(response.json())

def check_alerts():
    print("Checking active alerts...")
    response = requests.get(f"{BASE_URL}/alerts/active")
    print(response.json())

def check_analytics():
    print("Checking analytics...")
    response = requests.get(f"{BASE_URL}/analytics/hourly-speeds")
    print(response.json())

def main():
    # Wait for server to start
    time.sleep(2)
    
    print("--- Starting Verification ---")
    
    # Run ingestion multiple times to simulate data
    for _ in range(5):
        run_ingestion()
        time.sleep(1)
        
    check_alerts()
    check_analytics()
    
    print("--- Verification Complete ---")

if __name__ == "__main__":
    main()
