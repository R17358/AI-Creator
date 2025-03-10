import os
import cv2
import numpy as np
import random
import moviepy.editor as mp
from transitions import fade_in_transition, fade_to_black, crossfade_transition, dissolve_transition, glitch_transition, parallax_transition, whip_pan_transition, quick_cut_transition, water_ripple_transition, wipe_transition, zoom_transition


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

def create_video(image_paths, output_path, image_duration_list, transition_list=[], video_length=30, fps=30, transition_duration=1.5):
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
    
    frames.extend(fade_in_transition(images[0], transition_duration, fps))

    for i in range(len(images)-1):  
        img1 = cv2.resize(images[i], (width, height))
        img2 = cv2.resize(images[i + 1], (width, height))
        
        frames.extend([img1] * (round(image_duration_list[i]) * fps))  

        transition = transition_list[i].lower()

        if "fade in" in transition and i > 0:
            frames.extend(fade_in_transition(img1, transition_duration, fps))
        elif "fade to black" in transition or "fade out" in transition:
            frames.extend(fade_to_black(img1, transition_duration, fps))
        elif all(word in transition for word in ["cross", "fade"]):
            frames.extend(crossfade_transition(img1, img2, transition_duration, fps))
        elif "dissolve" in transition:
            frames.extend(dissolve_transition(img1, img2, transition_duration, fps))
        elif "glitch" in transition:
            frames.extend(glitch_transition(img1, img2, transition_duration, fps))
        elif "whip" in transition:
            frames.extend(whip_pan_transition(img1, img2, transition_duration, fps, "left"))
        elif all(word in transition for word in ["whip", "left"]):
            frames.extend(whip_pan_transition(img1, img2, transition_duration, fps, "left"))
        elif all(word in transition for word in ["whip", "right"]):
            frames.extend(whip_pan_transition(img1, img2, transition_duration, fps, "right"))
        elif "quick cut" in transition:
            frames.extend(quick_cut_transition(img1, img2, transition_duration, fps))
        elif any(word in transition for word in ["water", "ripple"]):
            frames.extend(water_ripple_transition(img1, img2, transition_duration, fps))
        elif all(word in transition for word in ["zoom", "in"]):
            frames.extend(zoom_transition(img1, img2, transition_duration, fps, "in"))
        elif all(word in transition for word in ["zoom", "out"]):
            frames.extend(zoom_transition(img1, img2, transition_duration, fps, "out"))
        elif "zoom" in transition:
            frames.extend(zoom_transition(img1, img2, transition_duration, fps, "in"))
        elif "parallax" in transition:
            frames.extend(parallax_transition(img1, img2, transition_duration, fps, "out"))
        else:
            frames.extend(crossfade_transition(img1, img2, transition_duration, fps))

    last_img = cv2.resize(images[-1], (width, height))  
    frames.extend([last_img] * (round(image_duration_list[-1]) * fps))
    frames.extend(fade_to_black(last_img, transition_duration, fps))

    # Ensure video length is at least `video_length`
    total_video_length = len(frames) / fps  # Get current video length

    if total_video_length < video_length:
        extra_frames_needed = (video_length - total_video_length) * fps
        print(f"Adding {int(extra_frames_needed)} extra frames to meet video length.")

        while len(frames) / fps < video_length:
            rand_idx = random.randint(0, len(images) - 1)  # Random image index
            rand_transition = random.choice(transition_list)  # Random transition
            img1 = images[rand_idx]
            img2 = images[random.randint(0, len(images) - 1)]  # Ensure next image is also random
            
            frames.extend([img1] * (fps * random.randint(2, 4)))  # Random extra duration

            # Apply a random transition
            if "fade in" in rand_transition:
                frames.extend(fade_in_transition(img1, transition_duration, fps))
            elif "fade to black" in rand_transition:
                frames.extend(fade_to_black(img1, transition_duration, fps))
            elif "cross fade" in rand_transition:
                frames.extend(crossfade_transition(img1, img2, transition_duration, fps))
            elif "dissolve" in rand_transition:
                frames.extend(dissolve_transition(img1, img2, transition_duration, fps))
            elif "glitch" in rand_transition:
                frames.extend(glitch_transition(img1, img2, transition_duration, fps))
            elif "zoom in" in rand_transition:
                frames.extend(zoom_transition(img1, img2, transition_duration, fps, "in"))
            elif "zoom out" in rand_transition:
                frames.extend(zoom_transition(img1, img2, transition_duration, fps, "out"))
            elif "parallax" in rand_transition:
                frames.extend(parallax_transition(img1, img2, transition_duration, fps, "out"))
            else:
                frames.extend(crossfade_transition(img1, img2, transition_duration, fps))

    # Save video
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    
    for frame in frames:
        out.write(frame)
    
    out.release()
    print("Video Generated")
    return output_path


# # **Example Usage**
# image_paths = [
#     "sample_test/Buddha.webp",
#     "sample_test/doraemon.webp",
#     "sample_test/durga ma.webp",
#     "sample_test/krishna.webp",
#     "sample_test/mogli.webp"
# ]
# transition_list = ["fade in", "ripple", "fade to black", "dissolve", "glitch"]  
# image_duration_list = [4.0, 4, 4, 4.2, 4] 
# output_path = "Generated_video/video.mp4"
# video_length = 70  # Ensure final video is at least 40 seconds long

# out = create_video(image_paths, output_path, image_duration_list, transition_list, video_length)
# print(out)
