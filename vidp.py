import streamlit as st
import os

# Streamlit app
def main():
    st.title("Video Upload and Playback")
    st.write("Upload a video file (MP4, AVI, etc.) and play it directly in the app.")

    # File uploader
    uploaded_file = st.file_uploader("Upload a video file", type=["mp4", "avi", "mov", "mkv"])

    if uploaded_file is not None:
        # Display the uploaded video
        st.video(uploaded_file)

        # Save the uploaded file to disk
        save_path = os.path.join("uploads", uploaded_file.name)
        os.makedirs("uploads", exist_ok=True)  # Create the "uploads" directory if it doesn't exist
        with open(save_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        # Display the file path
        st.write(f"**File saved at:** `{save_path}`")
        st.success("Video uploaded and saved successfully!")

# Run the app
if __name__ == "__main__":
    main()