# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Install system-level dependencies, including ffmpeg
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt and install dependencies
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application code to the container
COPY . /app

# Expose the default Streamlit port
EXPOSE 8501

# Command to run the Streamlit app
ENTRYPOINT ["streamlit", "run"]
CMD ["subtitles.py"]
