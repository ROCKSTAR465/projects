# SubNXT - Django Video Subtitle Generator

SubNXT is a web application built with Django that allows users to generate English subtitles for videos. It uses OpenAI's Whisper model for transcription and translation.

## Features
- Upload video files (MP4, AVI, MOV, MKV, etc.).
- Automatically generate English subtitles in WebVTT format (.vtt).
- Play back the video with embedded subtitles.
- Download the generated subtitle file.

## Prerequisites
- Python 3.8+
- Pip (Python package installer)
- FFmpeg: This is required by `openai-whisper` for audio extraction from videos.
  - **Linux (Debian/Ubuntu):** `sudo apt update && sudo apt install ffmpeg`
  - **MacOS (Homebrew):** `brew install ffmpeg`
  - **Windows:** Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/download.html) and add the `bin` directory to your system's PATH.

## Setup and Installation

1.  **Clone the Repository:**
    ```bash
    git clone <your_repository_url>
    cd <repository_directory>
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On Windows
    venv\Scripts\activate
    # On macOS/Linux
    source venv/bin/activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run Django Migrations (Initial Setup):**
    While this version doesn't use a complex database yet, it's good practice for Django projects.
    ```bash
    python subnxt_project/manage.py migrate
    ```
    *(Note: The project is named `subnxt_project`, so `manage.py` is inside it.)*

5.  **Run the Development Server:**
    ```bash
    python subnxt_project/manage.py runserver
    ```
    The application will typically be available at `http://127.0.0.1:8000/`.

## Usage
1. Open your web browser and navigate to `http://127.0.0.1:8000/`.
2. Click on "Choose video file" to select a video.
3. Click "Generate Subtitles".
4. The video will be processed, and you'll be taken to a results page where you can view the video with subtitles and download the .vtt file.

## Technical Details
- **Framework**: Django
- **Subtitle Generation**: OpenAI Whisper
- **Video Processing**: FFmpeg (via Whisper)
- **Subtitle Format**: WebVTT (.vtt)

---
*Replace `<your_repository_url>` and `<repository_directory>` with actual values if known, otherwise leave as placeholders.*
