# RTSP Stream Frame Capture

## Description

This project implements a web server using Flask that captures frames from RTSP video streams. The application allows users to start and stop streaming processes via HTTP endpoints, while also processing the frames to find and save the top 9 brightest frames as a grid image.

## Features

- Capture frames from multiple RTSP streams concurrently.
- Process frames to identify and save the 9 brightest frames as a grid image.
- Start and stop streams via HTTP endpoints.
- Display the generated image in an HTML response.

## Endpoints

- **`POST /start`**
  - **Parameters:**
    - `rtsp_url`: The URL of the RTSP stream to capture.
    - `interval`: (optional) The interval in seconds between frame captures (default is 1).
  - **Response:**
    - Confirmation message indicating that the video stream has started.

- **`POST /stop`**
  - **Parameters:**
    - `process_name`: The name of the stream process to stop.
  - **Response:**
    - An HTML page displaying the generated image of the top 9 brightest frames, or an error message if not enough frames were captured.

## Requirements

- Python 3.x
- Flask
- OpenCV
- NumPy
- Additional dependencies can be installed via `pip`.

## Installation

1. **Clone the repository:**

   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create a virtual environment (optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**

   ```bash
   pip install flask opencv-python numpy
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   python program.py
   ```

2. **Start capturing a stream:**

   ```bash
   curl -X POST -d "rtsp_url=<your_rtsp_url>&interval=1" http://localhost:8000/start
   ```

3. **Stop capturing a stream:**

   Send a POST request to /stop:
   
   ```bash
   curl -X POST -d "process_name=<your_process_name>" http://localhost:8000/stop
   ```

## Output

The application saves images of the top 9 brightest frames in the images directory. You can view these images by accessing the returned HTML response after stopping a stream.

## Logging

The application logs important events and errors to the console. Check the logs for details on frame capturing and processing.

## Docker Support

The application is designed to run inside Docker. You can build and run the Docker container using the following commands:

```bash
unzip exercise.zip
cd exercise
docker build -t exercise .
docker run -p 8000:8000 -v /path/to/exercise:/app exercise
```

## Example Commands

To start a stream:

```bash
curl -d "rtsp_url=rtsp://platerec:8S5AZ7YasGc3m4@video.platerecognizer.com:8554/demo" http://localhost:8000/start
```

To stop the stream and just save the file:

```bash
curl -X POST -d "process_name=demo" http://localhost:8000/stop
```

To stop the stream and view the file in a browser:

```bash
curl -X POST -d "process_name=demo" http://localhost:8000/stop -o response.html && google-chrome response.html
```

## Notes

Ensure that the RTSP URLs provided are accessible and valid.
The application supports multiple streams concurrently, allowing independent start/stop for each stream.
