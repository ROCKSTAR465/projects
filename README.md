# subtitles

!pip install openai-whisper

ensure that moviepy is installed in your local machine before running it locally

!pip install moviepy

Here’s a **README.md** file for your Streamlit app. This file provides an overview of your project, instructions for setting it up, and details on how to use it. You can customize it further based on your specific app features.

---

# Video Subtitle Generator with Whisper

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Whisper](https://img.shields.io/badge/OpenAI_Whisper-412991?style=for-the-badge&logo=openai&logoColor=white)

This is a **Streamlit app** that generates subtitles for video files using OpenAI's Whisper model. The app allows users to upload a video file, transcribe the audio, and generate subtitles in WebVTT format. The subtitles can be downloaded and displayed alongside the video.

---

## Features

- **Video Upload**: Upload video files in MP4 format.
- **Subtitle Generation**: Automatically generate subtitles using OpenAI's Whisper model.
- **Real-Time Playback**: Play the video with subtitles directly in the app.
- **Download Subtitles**: Download the generated subtitles in WebVTT format.

---

## Prerequisites

Before running the app, ensure you have the following installed:

- **Docker** (for containerized deployment)
- **Python 3.9+** (if running locally)
- **FFmpeg** (for audio/video processing)

---

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

### 2. Build the Docker Image

```bash
docker build -t streamlit-whisper-app .
```

### 3. Run the Docker Container

```bash
docker run -p 8501:8501 streamlit-whisper-app
```

### 4. Access the App

Open your browser and navigate to:

```
http://localhost:8501
```

---

## Usage

1. **Upload a Video**:
   - Click the "Upload a video file" button and select a video file (MP4 format).

2. **Generate Subtitles**:
   - The app will automatically transcribe the audio and generate subtitles.

3. **Play the Video**:
   - The video will play with subtitles displayed in real-time.

4. **Download Subtitles**:
   - Click the "Download Subtitles (VTT)" button to download the subtitles in WebVTT format.

---

## Configuration

### Environment Variables

You can configure the app using the following environment variables:

- `STREAMLIT_SERVER_PORT`: Port on which the app runs (default: `8501`).
- `STREAMLIT_SERVER_ENABLE_CORS`: Enable CORS (default: `false`).
- `STREAMLIT_SERVER_HEADLESS`: Run in headless mode (default: `true`).

---

## Technologies Used

- **Streamlit**: For building the web app.
- **OpenAI Whisper**: For transcribing audio and generating subtitles.
- **FFmpeg**: For processing video and audio files.
- **Docker**: For containerized deployment.

---

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a pull request.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **OpenAI** for the Whisper model.
- **Streamlit** for the amazing framework to build web apps.
- **FFmpeg** for audio/video processing.

---

## Contact

For questions or feedback, feel free to reach out:

- **Your Name**: [your-email@example.com](mailto:your-email@example.com)
- **GitHub**: [your-username](https://github.com/your-username)

---

Enjoy generating subtitles with ease! 🎥📝

---

### Customization Tips
- Replace `your-username`, `your-repo-name`, and `your-email@example.com` with your actual GitHub username, repository name, and email.
- Add screenshots or GIFs of your app to make the README more visually appealing.
- Include additional sections if your app has more features or configurations.

Let me know if you need further assistance! 😊
