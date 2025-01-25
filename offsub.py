import whisper
import os

# Function to generate subtitles
def generate_subtitles(video_path, output_path="subtitles.vtt", model_type="base"):
    try:
        # Load the Whisper model
        print(f"Loading Whisper model ({model_type})...")
        model = whisper.load_model(model_type)
        
        # Transcribe the video file (MP4)
        print(f"Transcribing {video_path}...")
        result = model.transcribe(video_path, task="translate")

        # Write subtitles to a WebVTT file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")  # WebVTT header
            for segment in result["segments"]:
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"]
                f.write(f"{start_time} --> {end_time}\n{text}\n\n")

        print(f"Subtitles saved to {output_path}")
        return True  # Indicate success
    except Exception as e:
        print(f"Error generating subtitles: {e}")
        return False  # Indicate failure

# Function to format timestamps
def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

# Main function
def main():
    # Input video file path
    video_path = input("Enter the path to the MP4 file: ").strip()

    # Check if the file exists
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return

    # Extract the base name of the video file (without extension)
    video_name = os.path.splitext(os.path.basename(video_path))[0]

    # Generate subtitle file name
    subtitle_file = f"{video_name}.vtt"

    # Generate subtitles
    if generate_subtitles(video_path, subtitle_file):
        print(f"Subtitles generated successfully and saved to '{subtitle_file}'.")
    else:
        print("Failed to generate subtitles.")

# Run the script
if __name__ == "__main__":
    main()