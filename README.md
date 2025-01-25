# **SubNXT - Generate Subtitles for Videos**

[Streamlit](https://subtitles.streamlit.app/) -click to open the web app

SubNXT is a Streamlit-based web application that allows users to generate English subtitles for videos in real-time. Powered by OpenAI's Whisper model, it can transcribe videos in any language and provide accurate translations into English. Users can upload a video, generate subtitles in WebVTT format, preview the video with subtitles, and download the generated subtitle file.

## **Features**
- 🎥 **Video Upload**: Upload MP4 video files for processing.
- 🔤 **Subtitle Generation**: Automatically transcribe and translate videos into English subtitles.
- 🖥️ **Video Playback with Subtitles**: Watch your video directly within the app, complete with subtitles.
- 📥 **Download Subtitles**: Download the generated subtitles as a `.vtt` file for future use.
- 🐍 Standalone Script: Use the provided Python script to generate subtitles locally without the web app.

---

## **How It Works**

### **Web App SubNXT**
1. Upload an MP4 video file.
2. The app processes the video using OpenAI's Whisper model.
3. Subtitles are generated and saved in WebVTT format.
4. The video is displayed with subtitles embedded, and the subtitle file can be downloaded.

### **Standalone Python Script offsub.py**
1. Run the Python script on your machine.
2. Provide the path to your video file.
3. Subtitles are generated and saved in the same directory as the input video.
### **Note:-**
  Download and install ffmpeg file in your machine and add the bin files to the system path variables.
  This is to ensure errorfree execution of the file.
---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/subnxt.git
cd subnxt
```

### **2. Install Dependencies**
Ensure you have Python 3.9+ installed (preferably python 3.11). Then, install the required dependencies:
```bash
pip install -r requirements.txt
```

### **3. Install FFmpeg**
FFmpeg is required for video processing. Install it using the appropriate method for your operating system:

- **Linux (Debian/Ubuntu):**
  ```bash
  sudo apt update
  sudo apt install ffmpeg
  ```

- **MacOS (Homebrew):**
  ```bash
  brew install ffmpeg
  ```

- **Windows:**
  1. Download FFmpeg from [ffmpeg.org](https://ffmpeg.org/).
  2. Add FFmpeg to your system PATH.

---

## **Usage**

### **1. Run the Web App**
Launch the Streamlit app locally:
```bash
streamlit run subtitles.py
```

Once the app is running, open your browser and go to:
```
http://localhost:8501
```

### **2. Use the Standalone Python Script**
Run the standalone script `offsub.py` to generate subtitles directly:
```bash
python offsub.py --video_path /path/to/video.mp4 --output_path /path/to/output.vtt --model_type base
```

#### **Script Options**
- `--video_path`: Path to the input video file.
- `--output_path`: (Optional) Path to save the subtitle file. Defaults to `subtitles.vtt` in the current directory.
- `--model_type`: (Optional) Whisper model type (`base`, `small`, `medium`, or `large`). Defaults to `base`.

---

## **Folder Structure**
```
subnxt/
├── subtitles.py          # Main Streamlit app
├── generate_subtitles.py # Standalone script for local subtitle generation
├── requirements.txt      # Python dependencies
├── uploads/              # Directory for uploaded files (created dynamically)
```

---

## **Technical Details**
- **Framework**: [Streamlit](https://streamlit.io/)
- **Model**: [OpenAI Whisper](https://github.com/openai/whisper)
- **Video Processing**: FFmpeg
- **Subtitle Format**: WebVTT (`.vtt`)

---

## **Future Improvements**
- Add support for more subtitle formats (e.g., SRT).
- Allow selection of transcription language.

---

## **License**
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## **Contributing**
Contributions are welcome! To contribute:
1. Fork this repository.
2. Create a feature branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Open a pull request.

---

## **Contact**
For any inquiries or issues, feel free to reach out:
- **Email**: kumaarsk390@gmail.com
- **GitHub**: [ROCKSTAR465](https://github.com/ROCKSTAR465)

---

### **Try SubNXT Today! 🚀**

---

### Example for `generate_subtitles.py`
```bash
python generate_subtitles.py --video_path example_video.mp4
```
Subtitles will be saved as `subtitles.vtt` in the current directory.

