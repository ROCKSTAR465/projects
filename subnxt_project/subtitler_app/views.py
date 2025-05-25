from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.conf import settings
import os
from .utils import generate_vtt_subtitles # Assuming utils.py is in the same app

def index_view(request):
    """
    Renders the main page where users can upload videos.
    """
    return render(request, 'subtitler_app/index.html')

def process_video_view(request):
    """
    Handles video upload, subtitle generation, and displays results.
    """
    if request.method == 'POST' and request.FILES.get('video_file'):
        video_file = request.FILES['video_file']
        
        fs = FileSystemStorage() # Uses MEDIA_ROOT by default for saving
        
        # Ensure media directory (and its subdirectories for videos if any) exists.
        # fs.save will typically create subdirectories if the name includes them,
        # but MEDIA_ROOT itself needs to exist.
        # os.makedirs(settings.MEDIA_ROOT, exist_ok=True) # Redundant if FileSystemStorage handles it, but safe.

        # Save uploaded video file directly into MEDIA_ROOT or a 'videos' subfolder
        # For simplicity, saving directly to MEDIA_ROOT as per fs.save behavior
        filename = fs.save(video_file.name, video_file) # filename is relative to MEDIA_ROOT
        uploaded_video_path = os.path.join(settings.MEDIA_ROOT, filename) # Absolute path
        uploaded_video_url = fs.url(filename) # URL relative to MEDIA_URL (e.g., /media/video.mp4)

        try:
            # Generate subtitles
            # utils.generate_vtt_subtitles now saves to MEDIA_ROOT/subtitles/ and returns absolute path
            vtt_file_abs_path = generate_vtt_subtitles(uploaded_video_path, model_type="base")
            
            # Construct the URL for the VTT file
            # vtt_file_abs_path is like /app/media/subtitles/video_name.vtt
            # MEDIA_ROOT is /app/media
            vtt_relative_path = os.path.relpath(vtt_file_abs_path, settings.MEDIA_ROOT)
            # vtt_relative_path will be 'subtitles/video_name.vtt'
            
            vtt_url = os.path.join(settings.MEDIA_URL, vtt_relative_path).replace("\\", "/")
            # vtt_url will be '/media/subtitles/video_name.vtt'

            context = {
                'video_url': uploaded_video_url,
                'vtt_url': vtt_url,
                'video_name': video_file.name,
                'vtt_filename': os.path.basename(vtt_file_abs_path) 
            }
            return render(request, 'subtitler_app/results.html', context)
        
        except FileNotFoundError as fnf_error:
            error_message = f"File not found during processing: {str(fnf_error)}"
            print(error_message) # Log error
            if fs.exists(filename):
                try:
                    fs.delete(filename)
                except Exception as del_e:
                    print(f"Error deleting orphaned file {filename}: {del_e}")
            context = {'error_message': error_message}
            return render(request, 'subtitler_app/index.html', context)

        except Exception as e:
            error_message = f"Failed to process video: {str(e)}"
            print(error_message) # Log error
            if fs.exists(filename):
                try:
                    fs.delete(filename)
                except Exception as del_e:
                    print(f"Error deleting orphaned file {filename}: {del_e}")
            context = {'error_message': error_message}
            return render(request, 'subtitler_app/index.html', context)

    # If not POST or no file, or other issues before try-except block in POST
    # This part handles GET requests or POST requests that don't meet the initial criteria
    # If it's a GET, simply render the index. If it's a POST that failed early, 
    # it might be better to show an error or just the plain form.
    # For simplicity, keeping it as rendering the index form without a specific error for GET.
    # If a POST request fails before `request.FILES.get('video_file')`, 
    # it will fall through here, which is fine.
    return render(request, 'subtitler_app/index.html')
