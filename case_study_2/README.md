# Vehicle Counting from Live Traffic Camera (Case Study 2)

This project is a Python backend service built with **FastAPI**, **MongoDB (Beanie ODM)**, **YOLOv8**, and **OpenCV** that processes a live YouTube traffic camera stream to detect and count vehicles moving in different directions.

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.10+
- MongoDB (running locally or remotely)
- FFmpeg (required for OpenCV/yt-dlp to process streams)

### Installation

1.  **Navigate to the Project Root** (`path_of_base_directory`):

    ```bash
    cd path_of_base_directory
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

    _Note: This will also install `ultralytics` and `opencv-python-headless`._

4.  **Configure Environment Variables**:
    - Navigate to the `case_study_2` directory:
      ```bash
      cd case_study_2
      ```
    - The project uses a `.env` file for configuration.
    - Ensure `MONGODB_URI` is set correctly in `.env`.
    - Example `.env`:
      ```env
      MONGODB_URI=mongodb://localhost:27017
      DB_NAME=vehicle_counting_db
      ```

## 🚀 How to Run

1.  **Start the Server**:

    - Make sure you are inside the `case_study_2` directory.
    - Run uvicorn using the virtual environment created in the root directory.

    ```bash
    ../venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
    ```

    - _Alternatively_, if you have activated the venv (`source ../venv/bin/activate`), you can just run:

    ```bash
    uvicorn app.main:app --host 0.0.0.0 --port 9000 --reload
    ```

2.  **Access the API**:

    - Open your browser and navigate to: [http://localhost:9000/docs](http://localhost:9000/docs)
    - This provides an interactive Swagger UI to test all endpoints.

3.  **Start Vehicle Counting**:

    - Use the `POST /start-processing` endpoint.
    - You can specify the `duration_minutes` (default is 3).
    - The server will start processing the video in the background.

4.  **Check Status**:
    - Use `GET /sessions` or `GET /sessions/{session_id}` to check the status and current counts.
    - Once completed, the status will change to `COMPLETED`.

## 🧠 Key Assumptions

1.  **Camera Angle**: The solution assumes a relatively static camera angle where a fixed horizontal and vertical line can effectively capture traffic flow.
2.  **YOLOv8 Nano**: We use the `yolov8n.pt` (Nano) model for real-time performance on CPU. While faster, it may be slightly less accurate than larger models (Small/Medium/Large).
3.  **Traffic Flow**:
    - **Incoming**: Vehicles moving Down (crossing horizontal line) or Right (crossing vertical line).
    - **Outgoing**: Vehicles moving Up (crossing horizontal line) or Left (crossing vertical line).
4.  **Counting Logic**: A vehicle is counted only when its centroid crosses the defined lines. A `counted_ids` set is used to prevent double counting the same vehicle ID.

## ⚠️ Known Limitations

1.  **Occlusion**: In heavy traffic, vehicles might block each other, leading to missed detections or ID switches (though YOLOv8 tracking handles this reasonably well).
2.  **Stream Lag**: Processing a live YouTube stream can sometimes introduce lag or connection drops (`Cannot reuse HTTP connection` warning), especially if the internet connection is unstable.
3.  **Night Accuracy**: The standard YOLO model is trained mostly on day-time images. Accuracy might drop significantly at night or in poor lighting conditions.
4.  **Processing Speed**: On a CPU, processing might be slower than real-time (FPS < 30), which is acceptable for counting but might result in skipped frames if not handled correctly.

## 🔮 Future Improvements

1.  **GPU Acceleration**: Deploy on a machine with a CUDA-enabled GPU to use larger YOLO models (e.g., `yolov8m.pt`) for higher accuracy and real-time FPS.
2.  **Zone-Based Counting**: Instead of simple lines, implement **Polygon Zones** (using `supervision` library or custom logic) to count vehicles entering/exiting specific complex intersection areas.
3.  **Class-Specific Counts**: Break down counts by vehicle type (e.g., Cars: 50, Trucks: 10, Buses: 5) instead of a total aggregate.
4.  **Cloud Storage**: Upload the processed output videos to S3/GCS instead of saving them locally, to make the system stateless and scalable.
