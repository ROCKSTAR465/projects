import whisper
import os
import time
import warnings  # Added to suppress warnings

# Suppress FP16 warning
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

#  ("tiny", "base", "small", "medium", "large").
def generate_subtitles(video_path, output_path, model_type):
    try:
        print(f"Loading Whisper model ({model_type})...")
        model = whisper.load_model(model_type)
        print(f"Transcribing {video_path}...")
        result = model.transcribe(video_path, task="translate")
        with open(output_path, "w", encoding="utf-8") as f:
            f.write("WEBVTT\n\n")
            for segment in result["segments"]:
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"]
                f.write(f"{start_time} --> {end_time}\n{text}\n\n")
        print(f"Subtitles saved to {output_path}")
        return True
    except Exception as e:
        print(f"Error generating subtitles: {e}")
        return False

def format_timestamp(seconds):
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def log_details(video_path, video_size, model_type, elapsed_time):
    log_file = "subtitles_log.txt"
    with open(log_file, "a", encoding="utf-8") as log:
        hours, remainder = divmod(elapsed_time, 3600)
        minutes, seconds = divmod(remainder, 60)
        log.write(f"Video File: {video_path}\n")
        log.write(f"Video Size: {video_size:.2f} MB\n")
        log.write(f"Model Used: {model_type}\n")
        log.write(f"Time Taken: {int(hours)}h {int(minutes)}m {int(seconds)}s\n")
        log.write("-" * 40 + "\n")

def main():
    start_time = time.time()
    video_path = input("Enter the path to the MP4 file: ").strip()
    if not os.path.exists(video_path):
        print(f"Error: The file '{video_path}' does not exist.")
        return
    
    video_size = os.path.getsize(video_path) / (1024 * 1024)  # Get video file size in MB
    print(f"Video file size: {video_size:.2f} MB")
    
    video_name = os.path.splitext(os.path.basename(video_path))[0]
    subtitle_file = f"{video_name}.vtt"
    model_type = "base"
    if generate_subtitles(video_path, subtitle_file, model_type=model_type):
        subtitle_size = os.path.getsize(subtitle_file) / (1024)  # Get subtitle file size in KB
        print(f"Subtitles generated successfully and saved to '{subtitle_file}'.")
        print(f"Subtitle file size: {subtitle_size:.2f} KB")
    else:
        print("Failed to generate subtitles.")
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    hours, remainder = divmod(elapsed_time, 3600)
    minutes, seconds = divmod(remainder, 60)
    print(f"Total execution time: {int(hours)}h {int(minutes)}m {int(seconds)}s")
    
    # Log details
    log_details(video_path, video_size, model_type, elapsed_time)

if __name__ == "__main__":
    main()
