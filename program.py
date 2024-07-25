from multiprocessing import Process, Manager, Event
import cv2
import logging
import numpy as np
import os
import time
from flask import Flask, request, render_template_string

# Initialize Flask app and multiprocessing manager
app = Flask(__name__)
manager = Manager()
frames = manager.dict()
termination_events = manager.dict()
processes = {}

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def capture_brigthest_frames(frames)
   return sorted(frames, key=lambda f: np.sum(f), reverse=True)[:9]

# Utility function to find and save the 9 brightest frames
def find_and_save_brightest_frames(process_name):
    if process_name not in frames or len(frames[process_name]) < 9:
        logger.warning(f"Not enough frames captured for process '{process_name}'")
        return None

    # Get top 9 brightest frames
    brightness_frames = capture_brigthest_frames(frames[process_name])

    # Create a 900x900 grid of the top frames
    grid_image = np.zeros((900, 900, 3), dtype=np.uint8)
    for i, frame in enumerate(brightness_frames):
        resized_frame = cv2.resize(frame, (300, 300))
        row, col = (i // 3) * 300, (i % 3) * 300
        grid_image[row:row + 300, col:col + 300] = resized_frame

    # Save the image
    os.makedirs('images', exist_ok=True)
    image_path = os.path.join('images', f"{process_name}.jpg")
    cv2.imwrite(image_path, grid_image)

    logger.info(f'Image saved at: {image_path}')
    return image_path

# Update shared frames dictionary
def update_shared_frames(process_name, frames_to_add):
    frames[process_name] = frames_to_add

# Check if the required number of frames have been captured
def required_frames_captured(frames_list):
    return len(frames_list) >= 9

# Capture frames from RTSP stream
def capture_frames(rtsp_url, interval, process_name, termination_event):
    cap = cv2.VideoCapture(rtsp_url)
    local_frames = []

    
    while cap.isOpened() and not termination_event.is_set():
        ret, frame = cap.read()
        if not ret:
            logger.error(f"Failed to read frame from {rtsp_url}")
            break

        local_frames.append(frame)
        if required_frames_captured(local_frames):
            update_shared_frames(process_name, local_frames)

        # Maintain a maximum of 100 frames
        if len(frames[process_name]) > 100:
            frames[process_name].pop(0)

        logger.info(f'Updated frames: {len(local_frames)}')
        time.sleep(interval)

    cap.release()
    update_shared_frames(process_name, local_frames)
    find_and_save_brightest_frames(process_name)

# Start a new stream processing
@app.route("/start", methods=["POST"])
def start_stream():
    rtsp_url = request.form.get("rtsp_url")
    interval = int(request.form.get("interval", 1))
    if not rtsp_url:
        return "Missing 'rtsp_url' parameter", 400

    process_name = os.path.basename(rtsp_url)
    if process_name in processes and processes[process_name].is_alive():
        return f"Stream '{process_name}' is already running", 400


    termination_event = Event()
    termination_events[process_name] = termination_event
    # Start a new process for capturing frames
    process = Process(target=capture_frames, args=(rtsp_url, interval, process_name, termination_event))
    processes[process_name] = process

    frames[process_name] = []
    process.start()
    logger.info(f"Started stream '{process_name}' with interval = {interval}")
    return f"Video stream started: '{process_name}'", 200

# Stop a running stream
@app.route("/stop", methods=["POST"])
def stop_stream():
    process_name = request.form.get("process_name")
    if not process_name:
        return "Missing 'process_name' parameter", 400

    if process_name not in processes:
        return f"No stream found for {process_name}", 400

    process = processes[process_name]
    if process.is_alive():
        if not required_frames_captured(frames.get(process_name, [])):
            return "Not enough frames captured", 400

        termination_event[process_name].set()    
        process.join()
        logger.info(f"Stream stopped: '{process_name}'")
    else:
        return f"Stream '{process_name}' is not running", 400

    # Save the brightest frames image
    image_path = find_and_save_brightest_frames(process_name)

    if prcess_termination_initiated:
        process.terminate()
    if not image_path:
        return "Not enough frames captured to generate image", 400

    return render_template_string(f'<html><body><img src="{image_path}" alt="image"></body></html>')

# Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
