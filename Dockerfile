# Base image with Python 3.11
FROM python:3.11

# Install dependencies
RUN apt-get update && apt-get install -y \
    libopencv-dev python3-opencv

# Copy project files
WORKDIR /app
COPY . /app

# Install Python dependencies
RUN python3 -m pip install --no-cache-dir -r requirements.txt

# Expose the port
EXPOSE 8000

# Set the default command
CMD ["python", "program.py"]
