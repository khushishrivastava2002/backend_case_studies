import cv2
from ultralytics import YOLO
import yt_dlp
import asyncio
from app.models import VehicleCountSession
from datetime import datetime
import os

class VideoProcessor:
    def __init__(self, session_id: str, video_url: str, duration_minutes: int = 3):
        self.session_id = session_id
        self.video_url = video_url
        self.duration_minutes = duration_minutes
        self.model = YOLO('yolov8n.pt')  # Load a pretrained YOLOv8n model
        self.output_path = f"output_{session_id}.mp4"
        self.counts = {"incoming": 0, "outgoing": 0}
        self.line_position = 0.5  # Horizontal line at 50% height
        self.tracked_ids = set()

    async def get_stream_url(self):
        ydl_opts = {'format': 'best'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(self.video_url, download=False)
            return info['url']

    async def process(self):
        session = await VehicleCountSession.get(self.session_id)
        if not session:
            return

        session.status = "PROCESSING"
        await session.save()

        try:
            stream_url = await self.get_stream_url()
            cap = cv2.VideoCapture(stream_url)
            
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            # Define counting lines
            line_y = int(height * self.line_position)
            line_x = int(width * 0.5)

            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            out = cv2.VideoWriter(self.output_path, fourcc, fps, (width, height))

            start_time = datetime.utcnow()
            frame_count = 0
            
            # Simple tracking state: {id: (prev_x, prev_y)}
            tracking_state = {}
            # Keep track of counted IDs to avoid double counting
            counted_ids = set()

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break

                current_time = datetime.utcnow()
                if (current_time - start_time).total_seconds() > self.duration_minutes * 60:
                    break

                # Run YOLO tracking
                results = self.model.track(frame, persist=True, classes=[2, 3, 5, 7], verbose=False)

                if results[0].boxes.id is not None:
                    boxes = results[0].boxes.xywh.cpu()
                    track_ids = results[0].boxes.id.int().cpu().tolist()
                    cls = results[0].boxes.cls.int().cpu().tolist()

                    for box, track_id, class_id in zip(boxes, track_ids, cls):
                        x, y, w, h = box
                        center_x = int(x)
                        center_y = int(y)
                        
                        if track_id in tracking_state:
                            prev_x, prev_y = tracking_state[track_id]
                            
                            # Check Horizontal Line Crossing (Up/Down)
                            if track_id not in counted_ids:
                                if prev_y < line_y and center_y >= line_y:
                                    self.counts["incoming"] += 1
                                    counted_ids.add(track_id)
                                elif prev_y > line_y and center_y <= line_y:
                                    self.counts["outgoing"] += 1
                                    counted_ids.add(track_id)
                                # Check Vertical Line Crossing (Left/Right)
                                elif prev_x < line_x and center_x >= line_x:
                                    self.counts["incoming"] += 1 # Map Right to Incoming
                                    counted_ids.add(track_id)
                                elif prev_x > line_x and center_x <= line_x:
                                    self.counts["outgoing"] += 1 # Map Left to Outgoing
                                    counted_ids.add(track_id)
                        
                        tracking_state[track_id] = (center_x, center_y)

                        # Draw bounding box and label
                        x1, y1, x2, y2 = int(x - w/2), int(y - h/2), int(x + w/2), int(y + h/2)
                        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                        cv2.putText(frame, f"ID: {track_id}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                # Draw counting lines
                cv2.line(frame, (0, line_y), (width, line_y), (0, 0, 255), 2)
                cv2.line(frame, (line_x, 0), (line_x, height), (255, 0, 0), 2)
                
                # Draw counts
                cv2.putText(frame, f"Incoming: {self.counts['incoming']}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
                cv2.putText(frame, f"Outgoing: {self.counts['outgoing']}", (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

                out.write(frame)
                frame_count += 1

            cap.release()
            out.release()

            session.end_time = datetime.utcnow()
            session.duration_seconds = (session.end_time - session.start_time).total_seconds()
            session.counts = self.counts
            session.video_path = self.output_path
            session.status = "COMPLETED"
            await session.save()

        except Exception as e:
            session.status = "FAILED"
            print(f"Error processing video: {e}")
            await session.save()
