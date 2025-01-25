# Use the official Python image as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Install system-level dependencies, including ffmpeg, and Python dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    && pip install --no-cache-dir -r requirements.txt \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy the entire application code into the container
COPY . /app

# Expose the default port for Streamlit
EXPOSE 8501

# Set the entrypoint to run the Streamlit app
ENTRYPOINT ["streamlit", "run"]

# Specify the main script of your app
CMD ["subtitles.py"]
