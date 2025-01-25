# Use Python 3.11 as the base image
FROM python:3.11-slim

# Set environment variables to avoid Streamlit runtime prompts
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_SERVER_PORT=8501 \
    STREAMLIT_SERVER_ENABLE_CORS=false \
    STREAMLIT_SERVER_HEADLESS=true

# Install system dependencies (FFmpeg and others)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libsndfile1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Verify FFmpeg installation
RUN ffmpeg -version

# Set the working directory inside the container
WORKDIR /app

# Copy requirements.txt and install Python dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code into the container
COPY . /app

# Expose the port Streamlit will run on
EXPOSE 8501

# Run the app with Streamlit
CMD ["streamlit", "run", "subtitles.py", "--server.port=8501", "--server.address=0.0.0.0"]
