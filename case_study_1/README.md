# Traffic Event & Analytics Service (Case Study 1)

This project is a Python backend service built with **FastAPI** and **MongoDB (Beanie ODM)** that ingests traffic signals and converts them into meaningful events and analytics. It simulates traffic data ingestion and implements stateful congestion detection logic.

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.10+
- MongoDB (running locally or remotely)

### Installation

1.  **Navigate to the Project Root** (`name_of_root_folder`):

    ```bash
    cd name_of_root_folder
    ```

2.  **Create a Virtual Environment**:

    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

4.  **Configure Environment Variables**:
    - Navigate to the `case_study_1` directory:
      ```bash
      cd case_study_1
      ```
    - The project uses a `.env` file for configuration.
    - Ensure `MONGODB_URL` is set correctly in `.env`.
    - Example `.env`:
      ```env
      MONGODB_URL=mongodb://localhost:27017
      DATABASE_NAME=traffic_analytics_db
      HERE_API_KEY=mock_key_for_now
      ```

## 🚀 How to Run

1.  **Start the Server**:

    - Make sure you are inside the `case_study_1` directory.
    - Run uvicorn using the virtual environment created in the root directory.

    ```bash
    ../venv/bin/uvicorn app.main:app --reload
    ```

    - _Alternatively_, if you have activated the venv (`source ../venv/bin/activate`), you can just run:

    ```bash
    uvicorn app.main:app --reload
    ```

2.  **Access the API**:

    - Open your browser and navigate to: [http://localhost:8000/docs](http://localhost:8000/docs)
    - This provides an interactive Swagger UI to test all endpoints.

3.  **Automatic Ingestion**:
    - The service includes a background scheduler that automatically ingests mock traffic data every **60 seconds** (configurable).
    - You can also manually trigger ingestion via `POST /ingest/run`.

## 🧠 Key Assumptions

1.  **Realistic Mock Data**: Since a live HERE Maps API key was not available, I implemented a smart mock data generator (`app/services/ingestion.py`). It generates correlated **Speed** and **Jam Factor** values:
    - High Jam Factor (e.g., 9.0) results in Low Speed.
    - Low Jam Factor (e.g., 1.0) results in High Speed (near Free Flow Speed).
2.  **Congestion Thresholds (Hysteresis)**:
    - **Congestion Start**: Jam Factor > 8.0 (High Congestion).
    - **Congestion End**: Jam Factor < 4.0 (Traffic Cleared).
    - **Stability Zone (4.0 - 8.0)**: To prevent event flickering, the status remains unchanged if the Jam Factor fluctuates within this range.
3.  **Location**: The service is currently configured for a single stretch: "Western Express Highway (Andheri-Bandra)".

## ⚠️ Known Limitations

1.  **Single Location**: The current implementation tracks a single hardcoded location. It can be easily extended to support multiple locations by accepting location ID in the ingestion payload.
2.  **Local Database**: Uses a local MongoDB instance. For production, a managed cluster (e.g., MongoDB Atlas) would be required.
3.  **No Authentication**: The API endpoints are currently public. In a real-world scenario, JWT or API Key authentication should be implemented.

## 🔮 Future Improvements

1.  **Real API Integration**: Replace the mock generator with the actual `httpx` client to fetch data from HERE Traffic API using the `HERE_API_KEY`.
2.  **Scalability**:
    - Offload data ingestion to a task queue like **Celery** or **Kafka** to handle high-throughput streams.
    - Use a Time-Series Database (e.g., **TimescaleDB** or **InfluxDB**) for more efficient storage and querying of historical traffic data.
3.  **Advanced Analytics**: Implement more complex aggregations, such as peak congestion hours and week-over-week comparisons.
4.  **Dockerization**: Containerize the application using Docker and Docker Compose for easier deployment.
