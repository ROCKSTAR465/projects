# Use Python 3.9 as the base image
FROM nuxeo:7.10

USER root

FROM python:3.9-slim

# Install system dependencies (FFmpeg)
# RUN apt-get update && apt-get install -y ffmpeg

# Verify FFmpeg installation
# RUN ffmpeg -version

# Copy requirements.txt and install Python dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

RUN echo "deb http://httpredir.debian.org/debian jessie non-free" >> /etc/apt/sources.list
RUN apt-get update && apt-get install -y --no-install-recommends libfaac-dev git

WORKDIR /tmp
# Build ffmpeg
ENV BUILD_YASM true
ENV LIBFAAC true
RUN git clone https://github.com/nuxeo/ffmpeg-nuxeo.git
WORKDIR ffmpeg-nuxeo
RUN ./prepare-packages.sh \
 && ./build-yasm.sh \
 && ./build-x264.sh \
 && ./build-libvpx.sh \
 && ./build-ffmpeg.sh \
 && cd /tmp \
 && rm -Rf ffmpeg-nuxeo \
 && rm -rf /var/lib/apt/lists/*

USER 1000
# Copy the app code
COPY . .

# Run the app
CMD ["streamlit", "run", "app.py"]




