import requests
import time

BASE_URL = "http://localhost:9000"

def test_api():
    print("Testing API...")
    
    # 1. Start Processing
    print("1. Starting processing...")
    response = requests.post(f"{BASE_URL}/start-processing", params={"duration_minutes": 1})
    if response.status_code == 200:
        session_id = response.json()["session_id"]
        print(f"   Success! Session ID: {session_id}")
    else:
        print(f"   Failed! {response.text}")
        return

    # 2. Check Status
    print("2. Checking status (waiting 10s)...")
    time.sleep(10)
    response = requests.get(f"{BASE_URL}/sessions/{session_id}")
    if response.status_code == 200:
        data = response.json()
        print(f"   Status: {data['status']}")
        print(f"   Counts: {data['counts']}")
    else:
        print(f"   Failed to get session! {response.text}")

    print("API Test Completed.")

if __name__ == "__main__":
    # Wait for server to start
    time.sleep(5)
    try:
        test_api()
    except Exception as e:
        print(f"Test failed: {e}")
