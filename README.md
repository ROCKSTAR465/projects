# **SubNXT - Generate Subtitles for Videos**

![Streamlit](https://subtitles.streamlit.app/)

SubNXT is a Streamlit-based web application that allows users to generate English subtitles for videos in real-time. Powered by OpenAI's Whisper model, it can transcribe videos in any language and provide accurate translations into English. Users can upload a video, generate subtitles in WebVTT format, preview the video with subtitles, and download the generated subtitle file.

## **Features**
- 🎥 **Video Upload**: Upload MP4 video files for processing.
- 🔤 **Subtitle Generation**: Automatically transcribe and translate videos into English subtitles.
- 🖥️ **Video Playback with Subtitles**: Watch your video directly within the app, complete with subtitles.
- 📥 **Download Subtitles**: Download the generated subtitles as a `.vtt` file for future use.

---

## **How It Works**
1. Upload an MP4 video file.
2. The app processes the video using OpenAI's Whisper model.
3. Subtitles are generated and saved in WebVTT format.
4. The video is displayed with subtitles embedded, and the subtitle file can be downloaded.

---

## **Installation**

### **1. Clone the Repository**
```bash
git clone https://github.com/your-username/subnxt.git
cd subnxt
```

### **2. Install Dependencies**
Ensure you have Python 3.9+ installed. Then, install the required dependencies:
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

### **1. Run the App**
Launch the Streamlit app locally:
```bash
streamlit run subtitles.py
```

### **2. Open the App in Your Browser**
Once the app is running, open your browser and go to:
```
http://localhost:8501
```

### **3. Upload a Video**
1. Drag and drop or select an MP4 video file to upload.
2. Wait while the app generates subtitles.

### **4. Preview and Download**
- Watch your video with subtitles embedded.
- Download the generated `.vtt` subtitle file.

---

## **Folder Structure**
```
subnxt/
├── subtitles.py          # Main Streamlit app
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

## **Example**
![App Screenshot](https://via.placeholder.com/800x400?text=Add+Screenshot)

---

## **Future Improvements**
- Add support for more subtitle formats (e.g., SRT).
- Allow selection of transcription language.
- Provide cloud deployment (e.g., Streamlit Community Cloud, AWS).
- Enable multi-user support for simultaneous processing.

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
- **Email**: your-email@example.com
- **GitHub**: [your-username](https://github.com/your-username)

---

### **Try SubNXT Today! 🚀**

---

**Next Steps:**
- **a.** Would you like help writing a `LICENSE` file for your project?  
- **b.** Do you want assistance deploying this app to a cloud platform like Streamlit Cloud or AWS?
