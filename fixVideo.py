import streamlit as st
import subprocess
import os

# # Input and output video paths
# input_video = "Generated_video/output_video.mp4"
# output_video = "Generated_video/output_fixed.mp4"

def fixVideoToShow(input_video, output_video):
    # Check if input video exists
    if not os.path.exists(input_video):
        print(f"❌ Input video not found: {input_video}")
    else:

        # FFmpeg command to re-encode the video
        ffmpeg_cmd = [
            "ffmpeg",
            "-i", input_video,       # Input file
            "-vcodec", "libx264",    # Encode in H.264 format
            "-acodec", "aac",        # Encode audio in AAC format
            "-strict", "experimental",
            output_video             # Output file
        ]

        # Run FFmpeg command
        try:
            st.info("⏳ Processing video, please wait...")
            subprocess.run(ffmpeg_cmd, check=True)
            st.success(f"✅ Video re-encoded successfully: {output_video}")

            # Load and display the fixed video
            with open(output_video, "rb") as video_file:
                video_bytes = video_file.read()

            return video_bytes  # Display in Streamlit
        except subprocess.CalledProcessError as e:
            return e
