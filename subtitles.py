import streamlit as st
import whisper
import os

# Function to generate subtitles
def generate_subtitles(video_path, output_path="subtitles.vtt", model_type="base"):
    try:
        # Load the Whisper model
        model = whisper.load_model(model_type)
        
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

# Streamlit app
def main():
    st.title("SubNXT")
    st.write("Generate English Subtitles from any language and play it with subtitles.")

    # File upload
    uploaded_file = st.file_uploader("Upload a video file (MP4)", type=["mp4"])
    # mp4_file_path = "uploads\480p.h264.mp4"
    if uploaded_file is not None:
        # Save the uploaded file
        mp4_file_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)  # Create the "uploads" directory if it doesn't exist
        with open(mp4_file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # st.write(f"File saved at: {mp4_file_path}")

        # Generate subtitles directly from the MP4 file
        subtitle_file = "subtitles.vtt"
        if generate_subtitles(mp4_file_path, subtitle_file):
            # Display the video with subtitles
            st.video(mp4_file_path, subtitles=subtitle_file)

            # Provide download link for subtitles
            with open(subtitle_file, "rb") as f:
                st.download_button(
                    label="Download Subtitles (VTT)",
                    data=f,
                    file_name=subtitle_file,
                    mime="text/vtt"
                )

# Run the app
if __name__ == "__main__":
    main()
