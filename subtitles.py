import streamlit as st
import whisper
import os
import tempfile
import time
import json
import base64
import warnings
warnings.filterwarnings("ignore", message="FP16 is not supported on CPU; using FP32 instead")

# Configure Streamlit page
st.set_page_config(
    page_title="SubNXT Pro: AI Subtitle Generator",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for modern UI with recommended color scheme
st.markdown("""
<style>
    /* Base styles with recommended color scheme */
    :root {
        --primary: #40e0d0;         /* Turquoise Green */
        --secondary: #0b1a3d;       /* Deep Midnight Blue */
        --accent: #3b9eff;          /* Neon Blue */
        --accent-alt: #9f5afd;      /* Electric Purple */
        --dark: #111111;            /* Charcoal Black */
        --light: #e0ffff;           /* Light Cyan */
        --light-alt: #f1f1f1;       /* Off-White */
        --error: #ff6b6b;           /* Coral Red */
        --warning: #f9c74f;         /* Golden Yellow */
        
        --gradient: linear-gradient(135deg, var(--primary) 0%, var(--accent-alt) 100%);
        --card-bg: rgba(17, 17, 17, 0.85);
        --title-gradient: linear-gradient(90deg, var(--primary), var(--accent-alt));
        --background-gradient: linear-gradient(135deg, var(--secondary) 0%, #0a142e 50%, #111111 100%);
    }
    
    /* Overall page styling */
    .stApp {
        background: var(--background-gradient);
        color: var(--light);
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    }
    
    /* Custom header with animation */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        text-align: center;
        background: var(--title-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 1rem 0;
        padding: 0.5rem;
        position: relative;
        animation: glow 3s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from {
            text-shadow: 0 0 5px rgba(64, 224, 208, 0.5), 
                         0 0 10px rgba(159, 90, 253, 0.3);
        }
        to {
            text-shadow: 0 0 15px rgba(64, 224, 208, 0.8), 
                         0 0 20px rgba(159, 90, 253, 0.6),
                         0 0 25px rgba(59, 158, 255, 0.4);
        }
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: rgba(11, 26, 61, 0.95) !important;
        border-right: 1px solid rgba(64, 224, 208, 0.3);
        backdrop-filter: blur(10px);
        box-shadow: 0 0 20px rgba(64, 224, 208, 0.3);
        padding: 1.5rem;
    }
    
    .sidebar-header {
        font-size: 1.8rem;
        font-weight: 700;
        background: var(--title-gradient);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1.5rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Cards styling */
    .card {
        background: var(--card-bg) !important;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid rgba(64, 224, 208, 0.2);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.5);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 24px rgba(64, 224, 208, 0.4);
        border-color: var(--primary);
    }
    
    .card-header {
        font-size: 1.4rem;
        font-weight: 600;
        color: var(--primary);
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Buttons styling */
    .stButton>button {
        background: var(--accent) !important;
        color: var(--secondary) !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 0.8rem 1.5rem !important;
        font-weight: 700 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 15px rgba(59, 158, 255, 0.4) !important;
    }
    
    .stButton>button:hover {
        background: var(--accent-alt) !important;
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(159, 90, 253, 0.6) !important;
    }
    
    .download-btn {
        background: linear-gradient(135deg, var(--primary) 0%, var(--accent-alt) 100%) !important;
        color: white !important;
    }
    
    /* Progress bar styling */
    .stProgress .st-bo {
        background: var(--primary) !important;
        border-radius: 10px;
        height: 12px !important;
    }
    
    .progress-container {
        background: rgba(17, 17, 17, 0.7);
        border-radius: 10px;
        padding: 1rem;
        margin: 1.5rem 0;
        border: 1px solid rgba(64, 224, 208, 0.3);
    }
    
    /* Video player container */
    .video-container {
        position: relative;
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 12px 24px rgba(0, 0, 0, 0.7);
        margin-bottom: 1.5rem;
        background: #000;
        border: 1px solid rgba(64, 224, 208, 0.3);
    }
    
    .video-player {
        width: 100%;
        display: block;
    }
    
    /* Subtitle display */
    .subtitle-display {
        position: absolute;
        bottom: 60px;
        left: 0;
        width: 100%;
        text-align: center;
        padding: 15px 0;
        background: rgba(17, 17, 17, 0.85);
        color: #a0f0ed; /* Light Turquoise */
        font-size: 1.8rem;
        font-weight: 600;
        text-shadow: 0 0 10px rgba(0,0,0,0.9);
        transition: all 0.3s ease;
        backdrop-filter: blur(5px);
        border-top: 1px solid rgba(64, 224, 208, 0.3);
        border-bottom: 1px solid rgba(64, 224, 208, 0.3);
    }
    
    /* Subtitle timeline */
    .subtitle-timeline {
        background: rgba(17, 17, 17, 0.85);
        padding: 15px;
        border-radius: 10px;
        margin-top: 20px;
    }
    
    .subtitle-item {
        background: rgba(64, 224, 208, 0.1);
        padding: 15px;
        border-radius: 10px;
        margin: 10px 0;
        border-left: 3px solid var(--primary);
        transition: all 0.3s ease;
    }
    
    .subtitle-item:hover {
        background: rgba(64, 224, 208, 0.2);
        transform: translateX(5px);
    }
    
    .subtitle-time {
        color: var(--primary);
        font-weight: 600;
        font-size: 1rem;
        margin-bottom: 5px;
    }
    
    .subtitle-text {
        font-size: 1.1rem;
        line-height: 1.5;
        color: var(--light);
    }
    
    /* File uploader */
    .stFileUploader>div>div {
        background: rgba(17, 17, 17, 0.7) !important;
        border: 2px dashed rgba(64, 224, 208, 0.5) !important;
        border-radius: 15px !important;
        padding: 2rem !important;
    }
    
    .stFileUploader>div>div:hover {
        border-color: var(--primary) !important;
        background: rgba(25, 25, 35, 0.8) !important;
    }
    
    /* Expander styling */
    .stExpander {
        background: rgba(17, 17, 17, 0.7) !important;
        border: 1px solid rgba(64, 224, 208, 0.3) !important;
        border-radius: 10px !important;
        margin-bottom: 0.8rem !important;
    }
    
    .stExpander summary {
        background: rgba(64, 224, 208, 0.15) !important;
        padding: 1rem !important;
        border-radius: 10px 10px 0 0 !important;
        font-weight: 600 !important;
        color: var(--primary) !important;
    }
    
    /* Footer styling */
    .footer {
        text-align: center;
        padding: 1.5rem;
        margin-top: 2rem;
        background: rgba(11, 26, 61, 0.7);
        border-radius: 15px;
        border-top: 1px solid rgba(64, 224, 208, 0.3);
    }
    
    /* Custom icons */
    .icon {
        font-size: 1.5rem;
        margin-right: 0.5rem;
        vertical-align: middle;
    }
    
    /* Neon glow effect for video container */
    .neon-glow {
        position: relative;
    }
    
    .neon-glow::before {
        content: '';
        position: absolute;
        top: -2px;
        left: -2px;
        right: -2px;
        bottom: -2px;
        background: var(--gradient);
        z-index: -1;
        filter: blur(15px);
        opacity: 0.5;
        border-radius: 14px;
    }
    
    /* Error messages */
    .stAlert {
        background-color: rgba(255, 107, 107, 0.15) !important;
        border-left: 4px solid var(--error) !important;
    }
    
    /* Success messages */
    .stSuccess {
        background-color: rgba(64, 224, 208, 0.15) !important;
        border-left: 4px solid var(--primary) !important;
    }
    
    /* Info messages */
    .stInfo {
        background-color: rgba(59, 158, 255, 0.15) !important;
        border-left: 4px solid var(--accent) !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'subtitles' not in st.session_state:
    st.session_state.subtitles = None
if 'video_path' not in st.session_state:
    st.session_state.video_path = None
if 'processing' not in st.session_state:
    st.session_state.processing = False
if 'current_subtitle' not in st.session_state:
    st.session_state.current_subtitle = ""
if 'font_size' not in st.session_state:
    st.session_state.font_size = 1.8
if 'position' not in st.session_state:
    st.session_state.position = "Bottom (Default)"

def format_timestamp(seconds):
    """Convert seconds to VTT timestamp format"""
    milliseconds = int((seconds - int(seconds)) * 1000)
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    return f"{hours:02}:{minutes:02}:{seconds:02}.{milliseconds:03}"

def generate_subtitles(video_path, model_type):
    """Generate subtitles using Whisper"""
    try:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        status_text.markdown(
            f'<div class="card"><div class="card-header"><span class="icon">⏳</span>Loading Whisper model...</div></div>',
            unsafe_allow_html=True
        )
        progress_bar.progress(20)
        model = whisper.load_model(model_type)
        
        status_text.markdown(
            f'<div class="card"><div class="card-header"><span class="icon">🎙️</span>Transcribing video...</div></div>',
            unsafe_allow_html=True
        )
        progress_bar.progress(40)
        result = model.transcribe(video_path, task="translate")
        
        status_text.markdown(
            f'<div class="card"><div class="card-header"><span class="icon">✍️</span>Processing subtitles...</div></div>',
            unsafe_allow_html=True
        )
        progress_bar.progress(80)
        
        # Format subtitles for display
        subtitles = []
        for segment in result["segments"]:
            subtitles.append({
                'start': segment["start"],
                'end': segment["end"],
                'text': segment["text"].strip()
            })
        
        progress_bar.progress(100)
        status_text.markdown(
            f'<div class="card"><div class="card-header"><span class="icon">✅</span>Subtitles generated successfully!</div></div>',
            unsafe_allow_html=True
        )
        time.sleep(1.5)
        progress_bar.empty()
        status_text.empty()
        
        return subtitles
        
    except Exception as e:
        st.error(f"Error generating subtitles: {str(e)}")
        return None

def get_subtitle_at_time(subtitles, current_time):
    """Get the subtitle text for the current time"""
    if not subtitles:
        return ""
    
    for subtitle in subtitles:
        if subtitle['start'] <= current_time <= subtitle['end']:
            return subtitle['text']
    return ""

def create_vtt_file(subtitles):
    """Create a VTT file content from subtitles"""
    vtt_content = "WEBVTT\n\n"
    for subtitle in subtitles:
        start_time = format_timestamp(subtitle['start'])
        end_time = format_timestamp(subtitle['end'])
        text = subtitle['text']
        vtt_content += f"{start_time} --> {end_time}\n{text}\n\n"
    return vtt_content

def get_base64_encoded_file(file_path):
    """Return base64 encoded file"""
    with open(file_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# Main UI
st.markdown('<h1 class="main-header">SubNXT Pro: AI Subtitle Generator</h1>', unsafe_allow_html=True)

# Sidebar for controls
with st.sidebar:
    st.markdown('<div class="sidebar-header"><span class="icon">🛠️</span>Configuration</div>', unsafe_allow_html=True)
    
    with st.container():
        st.markdown('<div class="card">', unsafe_allow_html=True)
        model_type = st.selectbox(
            "**Whisper Model**",
            ["tiny", "base", "small", "medium", "large"],
            index=2,
            help="Larger models are more accurate but slower"
        )
        
        st.markdown("""
        <div style="background: rgba(64, 224, 208, 0.15); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <h4 style="color: var(--primary); margin-bottom: 0.5rem;">Model Comparison:</h4>
            <ul style="padding-left: 1.5rem; color: var(--light);">
                <li><strong>Tiny</strong>: Fastest, basic accuracy</li>
                <li><strong>Base</strong>: Good balance</li>
                <li><strong>Small</strong>: Recommended for most users</li>
                <li><strong>Medium</strong>: High accuracy</li>
                <li><strong>Large</strong>: Best accuracy, slowest</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    # Features section
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h3 class="card-header"><span class="icon">✨</span>Features</h3>', unsafe_allow_html=True)
    st.markdown("""
    <div style="padding: 0.5rem 0; color: var(--light);">
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <span style="color: var(--primary); font-size: 1.5rem; margin-right: 10px;">✓</span>
            <span>Real-time subtitle display</span>
        </div>
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <span style="color: var(--primary); font-size: 1.5rem; margin-right: 10px;">✓</span>
            <span>Multi-format export</span>
        </div>
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <span style="color: var(--primary); font-size: 1.5rem; margin-right: 10px;">✓</span>
            <span>Subtitle editing</span>
        </div>
        <div style="display: flex; align-items: center; margin: 10px 0;">
            <span style="color: var(--primary); font-size: 1.5rem; margin-right: 10px;">✓</span>
            <span>Professional styling</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Main content area
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 class="card-header"><span class="icon">📤</span>Upload Media</h2>', unsafe_allow_html=True)

# File upload
uploaded_file = st.file_uploader(
    "Choose a video or audio file",
    type=['mp4', 'avi', 'mov', 'mkv', 'webm', 'm4v', 'mp3', 'wav', 'flac'],
    help="Upload your video or audio file to generate subtitles",
    label_visibility="collapsed"
)

if uploaded_file is not None:
    # Save uploaded file temporarily
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        video_path = tmp_file.name
        st.session_state.video_path = video_path
    
    # Display file info
    file_size = len(uploaded_file.getvalue()) / (1024 * 1024)
    st.success(f"📁 **File uploaded:** {uploaded_file.name} ({file_size:.2f} MB)")
    
    # Generate subtitles button
    if st.button("🚀 Generate Subtitles", type="primary", use_container_width=True):
        st.session_state.processing = True
        
        with st.spinner(""):
            st.markdown('<div style="text-align: center; font-size: 1.5rem; padding: 2rem; color: var(--primary);">Processing your media... ⚙️</div>', unsafe_allow_html=True)
            subtitles = generate_subtitles(video_path, model_type)
            if subtitles:
                st.session_state.subtitles = subtitles
                st.session_state.processing = False
                st.rerun()
                
st.markdown('</div>', unsafe_allow_html=True)  # Close card

# Display video with subtitles if available
if st.session_state.video_path and st.session_state.subtitles:
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-header"><span class="icon">🎥</span>Video with Synchronized Subtitles</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        # Create custom video player with subtitle display
        video_base64 = get_base64_encoded_file(st.session_state.video_path)
        video_ext = os.path.splitext(st.session_state.video_path)[1].replace(".", "")
        
        # Create HTML video player with subtitle display
        st.markdown(f"""
        <div class="video-container neon-glow">
            <video id="mainVideo" class="video-player" controls>
                <source src="data:video/{video_ext};base64,{video_base64}" type="video/{video_ext}">
            </video>
            <div id="subtitleDisplay" class="subtitle-display">
                {st.session_state.current_subtitle}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # JavaScript to sync subtitles with video
        subtitles_json = json.dumps(st.session_state.subtitles)
        st.markdown(f"""
        <script>
        const video = document.getElementById('mainVideo');
        const subtitleDisplay = document.getElementById('subtitleDisplay');
        const subtitles = {subtitles_json};
        
        video.addEventListener('timeupdate', function() {{
            const currentTime = video.currentTime;
            let currentSubtitle = '';
            
            for (let i = 0; i < subtitles.length; i++) {{
                const sub = subtitles[i];
                if (currentTime >= sub.start && currentTime <= sub.end) {{
                    currentSubtitle = sub.text;
                    break;
                }}
            }}
            
            subtitleDisplay.textContent = currentSubtitle;
        }});
        </script>
        """, unsafe_allow_html=True)
        
    with col2:
        st.markdown('<h3 class="card-header"><span class="icon">📝</span>Subtitle Controls</h3>', unsafe_allow_html=True)
        
        # Download VTT file
        vtt_content = create_vtt_file(st.session_state.subtitles)
        st.download_button(
            label="⬇️ Download VTT File",
            data=vtt_content,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}.vtt",
            mime="text/vtt",
            use_container_width=True
        )
        
        # Download JSON file
        json_content = json.dumps(st.session_state.subtitles, indent=2)
        st.download_button(
            label="⬇️ Download JSON",
            data=json_content,
            file_name=f"{os.path.splitext(uploaded_file.name)[0]}_subtitles.json",
            mime="application/json",
            use_container_width=True
        )
        
        # Subtitle settings
        st.markdown('<div style="margin-top: 2rem; background: rgba(64, 224, 208, 0.15); padding: 1rem; border-radius: 10px;">', unsafe_allow_html=True)
        st.markdown('<h4 style="color: var(--primary);"><span class="icon">⚙️</span>Subtitle Settings</h4>', unsafe_allow_html=True)
        
        # Font size slider
        font_size = st.slider("Font Size", 1.0, 3.0, st.session_state.font_size, 0.1, 
                             help="Adjust subtitle font size",
                             key="font_size_slider")
        st.session_state.font_size = font_size
        
        # Position selector
        position = st.selectbox("Position", 
                              ["Bottom (Default)", "Middle", "Top"],
                              index=0,
                              help="Position of subtitles on video",
                              key="position_select")
        st.session_state.position = position
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Update styles based on settings
        position_map = {
            "Bottom (Default)": "60px",
            "Middle": "50%",
            "Top": "100px"
        }
        st.markdown(f"""
        <style>
            .subtitle-display {{
                font-size: {font_size}rem;
                bottom: {position_map[position]};
            }}
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close card
    
    # Display subtitles timeline
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.markdown('<h2 class="card-header"><span class="icon">📋</span>Subtitle Timeline</h2>', unsafe_allow_html=True)
    
    # Create a scrollable container for subtitles
    subtitle_container = st.container()
    with subtitle_container:
        for i, subtitle in enumerate(st.session_state.subtitles):
            start_time = subtitle['start']
            end_time = subtitle['end']
            text = subtitle['text']
            
            # Format time display
            start_formatted = f"{int(start_time//60):02d}:{int(start_time%60):02d}"
            end_formatted = f"{int(end_time//60):02d}:{int(end_time%60):02d}"
            
            st.markdown(f"""
            <div class="subtitle-item">
                <div class="subtitle-time">🕒 {start_formatted} - {end_formatted}</div>
                <div class="subtitle-text">{text}</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)  # Close card

elif st.session_state.video_path and not st.session_state.subtitles and not st.session_state.processing:
    st.info("👆 Click 'Generate Subtitles' to create subtitles for your video!")

# Features section
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown('<h2 class="card-header"><span class="icon">✨</span>Why Choose SubNXT Pro?</h2>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 3rem; color: var(--primary);">⚡</div>
        <h3 style="color: var(--primary);">Real-Time Sync</h3>
        <p style="color: var(--light);">Subtitles displayed directly on your video with perfect timing</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 3rem; color: var(--accent);">🎯</div>
        <h3 style="color: var(--accent);">Professional Quality</h3>
        <p style="color: var(--light);">Cinema-style subtitles with customizable positioning and styling</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align: center; padding: 1.5rem;">
        <div style="font-size: 3rem; color: var(--accent-alt);">🎨</div>
        <h3 style="color: var(--accent-alt);">Easy Customization</h3>
        <p style="color: var(--light);">Adjust font size, position, and edit individual subtitles</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)  # Close card

# Footer
st.markdown("""
<div class="footer">
    <p style="color: var(--light);">Built with ❤️ using Streamlit and OpenAI Whisper • SubNXT Pro v2.0</p>
    <div style="display: flex; justify-content: center; gap: 1rem; margin-top: 1rem; font-size: 1.5rem;">
        <a href="#" style="color: var(--primary);">🌐 Website</a>
        <a href="#" style="color: var(--accent);">🐦 Twitter</a>
        <a href="#" style="color: var(--accent-alt);">💼 LinkedIn</a>
        <a href="#" style="color: var(--primary);">📧 Contact</a>
    </div>
</div>
""", unsafe_allow_html=True)
