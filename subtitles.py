from moviepy.editor import *

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

mp4_file_path = "/content/your_video.mp4"  # Replace with your MP4 file path
wav_file_path = "/content/your_audio.wav"  # Replace with desired WAV file path

convert_mp4_to_wav(mp4_file_path, wav_file_path)

import whisper

# Load the Whisper model
model = whisper.load_model("base")  # Options: "tiny", "small", "medium", "large"

# Transcribe the audio file
transcription = model.transcribe("New folder\Anime voice actor Akari Kito 360p.wav")

# Print the transcription
print("Transcription:", transcription["text"])

model = whisper.load_model("medium")  # You can choose "tiny", "base", "small", "medium", or "large"

# Step 4: Transcribe and translate the audio file
result = model.transcribe("/content/Anime voice actor Akari Kito 360p.wav", task="translate")  # Replace with your audio file path

print("Transcription in English:", result["text"])

