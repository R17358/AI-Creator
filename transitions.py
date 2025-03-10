import os
import cv2
import numpy as np
import moviepy.editor as mp
import random

def fade_in_transition(img, duration, fps):
    frames = []
    alpha_values = np.linspace(0, 1, int(duration * fps))
    black_frame = np.zeros_like(img)

    for alpha in alpha_values:
        blended = cv2.addWeighted(black_frame, 1 - alpha, img, alpha, 0)
        frames.append(blended)

    return frames

def fade_to_black(img, duration, fps):
    frames = []
    alpha_values = np.linspace(1, 0, int(duration * fps))  # Gradual fade out

    black_frame = np.zeros_like(img)  # Pure black frame

    for alpha in alpha_values:
        blended = cv2.addWeighted(img, alpha, black_frame, 1 - alpha, 0)
        frames.append(blended)

    return frames

def crossfade_transition(img1, img2, duration, fps):
    frames = []
    alpha_values = np.linspace(0, 1, int(duration * fps))
    for alpha in alpha_values:
        blended = cv2.addWeighted(img1, 1 - alpha, img2, alpha, 0)
        frames.append(blended)
    return frames

def dissolve_transition(img1, img2, duration, fps):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)
    
    # Create an ordered mask sequence for smoother pixel replacement
    pixel_indices = np.array([(x, y) for x in range(height) for y in range(width)])
    np.random.shuffle(pixel_indices)  # Randomize order of pixel replacement
    
    for i in range(1, num_frames + 1):
        num_pixels_to_change = int((i / num_frames) * len(pixel_indices))
        mask = np.zeros((height, width), dtype=np.uint8)
        
        # Reveal more pixels gradually
        for x, y in pixel_indices[:num_pixels_to_change]:
            mask[x, y] = 1  # Mark pixel as belonging to img2
        
        blended = np.where(mask[:, :, None] == 1, img2, img1)  # Apply mask
        frames.append(blended)

    return frames


def water_ripple_transition(img1, img2, duration, fps):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)
    center_x, center_y = width // 2, height // 2
    max_radius = min(width, height) // 2

    for i in range(1, num_frames + 1):
        frame = img1.copy()
        
        # Create a coordinate grid for the entire image
        y, x = np.meshgrid(np.arange(height), np.arange(width), indexing='ij')
        dx, dy = x - center_x, y - center_y
        distance = np.sqrt(dx**2 + dy**2)
        
        # Generate a ripple effect based on the distance from the center
        ripple_strength = (i / num_frames) * max_radius  # Expanding ripple size
        wave_offset = (10 * np.sin(distance / 15 - i * 0.3)).astype(np.int32)  # Sinusoidal wave
        
        # Apply distortion
        new_x = np.clip(x + wave_offset, 0, width - 1)
        new_y = np.clip(y + wave_offset, 0, height - 1)
        
        # Map pixels from img1 using distorted coordinates
        frame = img1[new_y, new_x]
        
        # Gradually blend into img2
        alpha = i / num_frames
        blended = cv2.addWeighted(frame, 1 - alpha, img2, alpha, 0)
        frames.append(blended)

    return frames

def quick_cut_transition(img1, img2, duration, fps):
    frames = []
    num_frames = int(duration * fps)

    # Display the first image for half the duration
    frames.extend([img1] * (num_frames // 2))

    # Instant cut to the second image
    frames.extend([img2] * (num_frames // 2))

    return frames

def wipe_transition(img1, img2, duration, fps, direction="left"):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)

    for i in range(num_frames + 1):
        frame = img1.copy()
        progress = int((i / num_frames) * width)  # Progress of wipe effect

        if direction == "left":
            frame[:, :progress] = img2[:, :progress]  # Wipe from left to right
        elif direction == "right":
            frame[:, width - progress:] = img2[:, width - progress:]  # Wipe from right to left
        elif direction == "top":
            frame[:progress, :] = img2[:progress, :]  # Wipe from top to bottom
        elif direction == "bottom":
            frame[height - progress:, :] = img2[height - progress:, :]  # Wipe from bottom to top

        frames.append(frame)

    return frames


def glitch_transition(img1, img2, duration, fps):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)

    for i in range(num_frames):
        frame = img1.copy()

        # Apply random horizontal shifts (glitch effect)
        for _ in range(10):  # Number of glitch lines
            y = random.randint(0, height - 1)
            shift = random.randint(-40, 50)
            frame[y, :] = np.roll(frame[y, :], shift, axis=0)

        # Add RGB channel split effect
        if i % 5 == 0:  # Every 5th frame has a stronger RGB shift
            b, g, r = cv2.split(frame)
            b = np.roll(b, random.randint(-5, 5), axis=1)
            g = np.roll(g, random.randint(-5, 5), axis=0)
            r = np.roll(r, random.randint(-5, 5), axis=1)
            frame = cv2.merge([b, g, r])

        # Add noise
        noise = np.random.randint(0, 50, (height, width, 3), dtype=np.uint8)
        frame = cv2.addWeighted(frame, 0.9, noise, 0.1, 0)

        # Gradually blend into the next image
        alpha = i / num_frames
        blended = cv2.addWeighted(frame, 1 - alpha, img2, alpha, 0)
        frames.append(blended)

    return frames

def zoom_transition(img1, img2, duration, fps, direction):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)

    for i in range(num_frames):
        alpha = i / num_frames  # Progress of transition

        # Zooming effect: Resize img1 dynamically
        if direction == "in":
            scale_factor = 1 + alpha * 1.5  # Increase scale smoothly
        else:
            scale_factor = 1.5 - alpha * 0.5  # Decrease scale smoothly (Zoom Out)
            
        resized_img1 = cv2.resize(img1, None, fx=scale_factor, fy=scale_factor)

        # Crop to original size (centered)
        start_x = (resized_img1.shape[1] - width) // 2
        start_y = (resized_img1.shape[0] - height) // 2
        cropped_img1 = resized_img1[start_y:start_y+height, start_x:start_x+width]

        # Blend into img2 gradually
        blended = cv2.addWeighted(cropped_img1, 1 - alpha, img2, alpha, 0)
        frames.append(blended)

    return frames

def whip_pan_transition(img1, img2, duration, fps, direction="right"):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)
    
    for i in range(1, num_frames + 1):
        shift = int((i / num_frames) * width)  # Shift amount

        if direction == "right":
            frame = np.zeros_like(img1)
            frame[:, :width-shift] = img1[:, shift:]  # Move left
            frame[:, width-shift:] = img2[:, :shift]  # Bring next image from right
        elif direction == "left":
            frame = np.zeros_like(img1)
            frame[:, shift:] = img1[:, :width-shift]  # Move right
            frame[:, :shift] = img2[:, width-shift:]  # Bring next image from left
        elif direction == "up":
            frame = np.zeros_like(img1)
            frame[:height-shift, :] = img1[shift:, :]  # Move up
            frame[height-shift:, :] = img2[:shift, :]  # Bring next image from bottom
        elif direction == "down":
            frame = np.zeros_like(img1)
            frame[shift:, :] = img1[:height-shift, :]  # Move down
            frame[:shift, :] = img2[height-shift:, :]  # Bring next image from top

        frames.append(frame)

    return frames

def cloth_effect_transition(img1, img2, duration, fps):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)

    for i in range(1, num_frames + 1):
        frame = img1.copy()
        wave_amplitude = int(20 * (1 - i / num_frames))  # Decreasing wave intensity
        
        for y in range(height):
            offset = int(wave_amplitude * np.sin(2 * np.pi * y / 50 + i * 0.2))  # Sinusoidal wave
            new_x = np.clip(np.arange(width) + offset, 0, width - 1)  # Shift pixels
            frame[y, :] = img1[y, new_x]  # Apply wave distortion
        
        # Blend into the second image
        alpha = i / num_frames
        blended = cv2.addWeighted(frame, 1 - alpha, img2, alpha, 0)
        frames.append(blended)

    return frames


def parallax_transition(img1, img2, duration, fps):
    frames = []
    height, width, _ = img1.shape
    num_frames = int(duration * fps)

    for i in range(num_frames):
        alpha = i / num_frames  # Blending factor

        # Shift foreground faster (closer)
        foreground_shift = int((1 - alpha) * width * 0.3)  # Moves 30% of the width
        bg_shift = int((1 - alpha) * width * 0.1)  # Background moves 10% of width

        # Create shifted versions of images
        foreground = np.zeros_like(img1)
        background = np.zeros_like(img2)

        # Apply shifting effect
        if foreground_shift > 0:
            foreground[:, foreground_shift:] = img1[:, :-foreground_shift]
        else:
            foreground = img1

        if bg_shift > 0:
            background[:, :-bg_shift] = img2[:, bg_shift:]
        else:
            background = img2

        # Blend background and foreground with transparency
        blended = cv2.addWeighted(foreground, 1 - alpha, background, alpha, 0)
        frames.append(blended)

    return frames


