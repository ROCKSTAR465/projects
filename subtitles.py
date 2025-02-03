import streamlit as st
import whisper
import os
import tempfile
import base64

# Function to generate subtitles
def generate_subtitles(video_path, output_path="subtitles.vtt", model_type="base"):
    try:
        # Load the Whisper model
        model = whisper.load_model(model_type, device="cuda")
        
        # Transcribe the video file (MP4)
        result = model.transcribe(video_path, task="translate")

        # Write subtitles to a WebVTT file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")  # WebVTT header
            for segment in result["segments"]:
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"]
                f.write(f"{start_time} --> {end_time}\n{text}\n\n")

        st.success(f"Subtitles saved to {output_path}")
        return True  # Indicate success
    except Exception as e:
        st.error(f"Error generating subtitles: {e}")
        return False  # Indicate failure

# Function to format timestamps
def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Function to encode file content as base64
def encode_file_to_base64(file_path):
    with open(file_path, "rb") as file:
        return base64.b64encode(file.read()).decode("utf-8")

# Streamlit app
def main():
    st.title("SubNXT")
    st.write("Generate English Subtitles from any language and play it with subtitles.")

    # File upload
    uploaded_file = st.file_uploader("Upload a video file (MP4, AVI, MOV, MKV)", type=["mp4", "avi", "mov", "mkv"])
    if uploaded_file is not None:
        # Save the uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as temp_video:
            temp_video.write(uploaded_file.getbuffer())
            video_path = temp_video.name

        # Generate subtitles and save temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=".vtt") as temp_subtitle:
            subtitle_path = temp_subtitle.name

        # Generate subtitles
        if generate_subtitles(video_path, subtitle_path):
            # Encode video and subtitles for embedding
            video_base64 = encode_file_to_base64(video_path)
            subtitle_base64 = encode_file_to_base64(subtitle_path)

            # Embed video and subtitles using custom HTML
            video_html = f"""
            <video width="640" height="360" controls>
                <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                <track src="data:text/vtt;base64,{subtitle_base64}" kind="subtitles" srclang="en" label="English" default>
                Your browser does not support the video tag.
            </video>
            """
            st.components.v1.html(video_html, height=400)

            # Provide download link for subtitles
            with open(subtitle_path, "rb") as f:
                st.download_button(
                    label="Download Subtitles (VTT)",
                    data=f,
                    file_name="subtitles.vtt",
                    mime="text/vtt"
                )

if __name__ == "__main__":
    main()
