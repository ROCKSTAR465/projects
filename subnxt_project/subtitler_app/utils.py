import whisper
import os
import tempfile
import torch # Added for device selection
import warnings
from django.conf import settings # Added for MEDIA_ROOT

# Suppress FP16 warning, similar to Offline.py
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

def format_timestamp(seconds):
    """Converts seconds to VTT timestamp format."""
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds_val = int(seconds % 60) # Renamed to avoid conflict with module
    return f"{hours:02}:{minutes:02}:{seconds_val:02}.{milliseconds:03}"

def generate_vtt_subtitles(video_file_path: str, model_type: str = "base") -> str:
    """
    Generates VTT subtitles from a video file and returns the path to the VTT file.

    Args:
        video_file_path: Path to the video file.
        model_type: Name of the Whisper model to use (e.g., "tiny", "base", "small").

    Returns:
        Path to the generated VTT file.

    Raises:
        FileNotFoundError: If the video_file_path does not exist.
        Exception: If any other error occurs during subtitle generation.
    """
    if not os.path.exists(video_file_path):
        raise FileNotFoundError(f"Video file not found: {video_file_path}")

    try:
        # Check if CUDA is available, similar to subtitles.py
        device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Load the Whisper model
        model = whisper.load_model(model_type, device=device)
        
        # Transcribe the video file
        result = model.transcribe(video_file_path, task="translate") # "translate" to English

        # Define output directory and filename
        video_basename = os.path.splitext(os.path.basename(video_file_path))[0]
        output_filename = f"{video_basename}.vtt"
        
        vtt_dir = os.path.join(settings.MEDIA_ROOT, 'subtitles')
        os.makedirs(vtt_dir, exist_ok=True) # Ensure the directory exists
        
        output_path = os.path.join(vtt_dir, output_filename)

        # Write VTT content to the specified output path
        with open(output_path, "w", encoding="utf-8") as vtt_file:
            vtt_file.write("WEBVTT\n\n")
            for segment in result["segments"]:
                start_time = format_timestamp(segment["start"])
                end_time = format_timestamp(segment["end"])
                text = segment["text"].strip() # Added strip() for cleaner text
                vtt_file.write(f"{start_time} --> {end_time}\n{text}\n\n")
        
        return output_path

    except Exception as e:
        # If an error occurs, attempt to clean up the output file if it was created
        if 'output_path' in locals() and os.path.exists(output_path):
            try:
                os.remove(output_path)
            except OSError: # Handle cases where file might be locked or other issues
                pass 
        # Re-raise the exception to be handled by the caller
        raise Exception(f"Error generating subtitles for {video_file_path} using {model_type} model: {e}")

if __name__ == '__main__':
    # This is a simple test case, normally this would be part of a test suite
    # To run this, you'd need a dummy video file or a small actual video file.
    # For now, this part is illustrative and won't be executed in the agent's environment.
    print("Attempting to generate subtitles (this is a test within utils.py)...")
    # Create a dummy video file for testing if it doesn't exist
    dummy_video_path = "dummy_video.mp4"
    if not os.path.exists(dummy_video_path):
        with open(dummy_video_path, "w") as f:
            f.write("dummy video content") # Whisper might not process this, but it's for path testing

    try:
        # NOTE: Whisper will likely fail on a dummy text file. 
        # This test is more about the file path handling and function signature.
        # A proper test would mock the whisper library or use a very small, valid audio/video file.
        print(f"Testing with dummy file: {dummy_video_path}")
        # vtt_path = generate_vtt_subtitles(dummy_video_path, model_type="tiny")
        # print(f"Generated VTT file (dummy test): {vtt_path}")
        # if os.path.exists(vtt_path):
        #     with open(vtt_path, "r", encoding="utf-8") as f_read:
        #         print("VTT content (dummy test):")
        #         print(f_read.read())
        #     os.remove(vtt_path) # Clean up dummy VTT
        print("Skipping actual whisper call in dummy test to avoid errors with invalid file.")
        print("To test properly, replace dummy_video.mp4 with a real (small) video and uncomment calls.")

    except FileNotFoundError as fnf_error:
        print(f"Test Error: {fnf_error}")
    except Exception as e:
        print(f"An error occurred during the test: {e}")
    finally:
        if os.path.exists(dummy_video_path):
            # os.remove(dummy_video_path) # Clean up dummy video
            print(f"Kept dummy file {dummy_video_path} for potential manual inspection.")
            pass
    print("utils.py test section finished.")
