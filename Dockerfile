# Use Python 3.11 as the base image
FROM python:3.9-slim

# Install system dependencies (FFmpeg)
RUN apt-get update && apt-get install -y ffmpeg

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV PATH="/usr/bin/ffmpeg:${PATH}"

# Copy the app code
COPY . .

# Run the app
CMD ["streamlit", "run", "app.py"]
