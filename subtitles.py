import whisper
import os
from moviepy.editor import *

def generate_subtitles(video_path, output_path="subtitles.vtt", model_type="medium"):
    """
    Generate subtitles in WebVTT format using Whisper.

    Args:
        video_path (str): Path to the video/audio file.
        output_path (str): Path to save the output .vtt subtitle file.
        model_type (str): Type of Whisper model to use ("tiny", "base", "small", "medium", "large").
    """
    # Load the Whisper model
    print(f"Loading Whisper model ({model_type})...")
    model = whisper.load_model(model_type)

    # Transcribe the audio
    print(f"Transcribing {video_path}...")
    result = model.transcribe(video_path, task="translate")

    # Generate WebVTT format
    print("Generating subtitles in WebVTT format...")
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("WEBVTT\n\n")  # WebVTT header

        for segment in result["segments"]:
            # Convert timestamps to WebVTT format (hh:mm:ss.mmm)
            start_time = format_timestamp(segment["start"])
            end_time = format_timestamp(segment["end"])
            text = segment["text"]

            # Write each subtitle block
            f.write(f"{start_time} --> {end_time}\n{text}\n\n")

    print(f"Subtitles saved to {output_path}")


def format_timestamp(seconds):
    """
    Format seconds into WebVTT timestamp (hh:mm:ss.mmm).

    Args:
        seconds (float): Time in seconds.

    Returns:
        str: Formatted timestamp.
    """
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"



def convert_mp4_to_wav(mp4_file, wav_file):
    """Converts an MP4 file to a WAV file.

    Args:
        mp4_file: Path to the input MP4 file.
        wav_file: Path to the output WAV file.
    """
    try:
        video = VideoFileClip(mp4_file)
        audio = video.audio
        audio.write_audiofile(wav_file)
        video.close()
        audio.close()
        print(f"Successfully converted {mp4_file} to {wav_file}")
    except Exception as e:
        print(f"Error converting {mp4_file}: {e}")

mp4_file_path = "/content/480p.h264.mp4"  # Replace with your MP4 file path
wav_file_path = "/content/480p.wav"  # Replace with desired WAV file path

convert_mp4_to_wav(mp4_file_path, wav_file_path)

# Audio file path automation

def process_video_folder(folder_path):
    """
    Process all video files in the given folder.

    Args:
        folder_path (str): Path to the folder containing video files.
    """
    # Supported video formats
    supported_formats = (".mp4", ".mkv", ".avi", ".mov", ".flv", ".wmv")

    # Iterate through all files in the folder
    for file_name in os.listdir(folder_path):
        if file_name.endswith(supported_formats):
            video_path = os.path.join(folder_path, file_name)
            wav_file = os.path.splitext(video_path)[0] + ".wav"
            subtitle_file = os.path.splitext(video_path)[0] + ".vtt"

            print(f"\nProcessing video: {file_name}")
            convert_mp4_to_wav(video_path, wav_file)
            generate_subtitles(wav_file, subtitle_file)


if __name__ == "__main__":
    # Input video/audio file path

    video_path = wav_file_path

    # Output subtitle file path
    output_path = "subtitles.vtt"

    # Generate subtitles
    generate_subtitles(video_path, output_path)
