# Use Python 3.9 as the base image
FROM python:3.9-slim

# Install system dependencies (FFmpeg)
RUN apt-get update && apt-get install -y ffmpeg

# Verify FFmpeg installation
RUN ffmpeg -version

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the app code
COPY . .

# Run the app
CMD ["streamlit", "run", "subtitles.py"]
