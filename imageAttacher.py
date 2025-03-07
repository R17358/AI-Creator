import os
import cv2
import numpy as np
import moviepy.editor as mp

def crossfade_transition(img1, img2, duration, fps):
    frames = []
    alpha_values = np.linspace(0, 1, int(duration * fps))
    for alpha in alpha_values:
        blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
        frames.append(blended)
    return frames

def create_video(image_paths, output_path, fps=30, image_duration_list=[], transition_duration=1):
    
    frames = []
    images = []
    
    for img_path in image_paths:
        if not os.path.exists(img_path):
            print(f"Error: File not found - {img_path}")
            continue
        img = cv2.imread(img_path)
        if img is None:
            print(f"Error: Could not read image - {img_path}")
            continue
        images.append(img)
    
    if len(images) < 2:
        print("Error: Not enough valid images to create a video.")
        return None
    
    height, width, _ = images[0].shape
    
    for i in range(len(images)):
        img = cv2.resize(images[i], (width, height))
        frames.extend([img] * (round(image_duration_list[i]) * fps))
        if i < len(images) - 1:
            frames.extend(crossfade_transition(images[i], images[i + 1], transition_duration, fps))
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    for frame in frames:
        out.write(frame)
    out.release()
    print("Video Generated")
    return output_path

def add_music_to_video(video_path, audio_path, output_video_path):
    if not os.path.exists(video_path):
        print("Error: Video file not found.")
        return None
    if not os.path.exists(audio_path):
        print("Error: Audio file not found.")
        return None
    
    video = mp.VideoFileClip(video_path)
    audio = mp.AudioFileClip(audio_path).set_duration(video.duration)
    video_with_audio = video.set_audio(audio)
    video_with_audio.write_videofile(output_video_path, codec="libx264", audio_codec="aac")
    print("Video with music generated")
    return output_video_path
