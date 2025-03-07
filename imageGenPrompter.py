import google.generativeai as genai
import os
import time
import re
import streamlit as st
from dotenv import load_dotenv
import markdown2

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')


def remove_code_block_markers(text: str) -> str:
    """
    Removes markdown code block markers from the beginning and end of a string.
    
    Parameters:
        text (str): The input string potentially wrapped in code block markers.
        
    Returns:
        str: The cleaned string without the code block markers.
    """
    text = text.strip()  # Remove leading/trailing whitespace

    # Remove starting marker if present
    if text.startswith("```json"):
        text = text[len("```json"):].strip()
    elif text.startswith("```"):
        text = text[len("```"):].strip()
        
    # Remove ending marker if present
    if text.endswith("```"):
        text = text[:-len("```")].strip()
        
    return text


def renderMarkDown(md_text):
    rendered_text = markdown2.markdown(md_text)
    return rendered_text

def clean_markdown(md_text):
    return re.sub(r'(\*{1,2}|_|\#)', '', md_text)

def imgPrompt(user_input, numOfPrompts):

# 6. **Number of Prompts for Image generation should be {numOfPrompts}. and all images should be contextual.
# add this line when want  to set more number of images or length
    
    system_instruction = f"""
    You are an **AI expert in music, song and lyrics writing, image prompt generation, video editing, and cinematic storytelling**. Your primary goal is to **analyze song lyrics, break them into emotionally significant parts, and generate highly detailed AI image prompts** that capture the theme, mood, and atmosphere of each segment. You also ensure that **each visual aligns perfectly with the song's emotions and storytelling, creating a seamless cinematic experience**.

    ### **Responsibilities:**
    1. **Creative Lyrics Segmentation**:
    - Break down song lyrics into **emotionally significant segments** based on transitions in mood, story, or energy.
    - Ensure each segment has a **distinct narrative purpose** that enhances the song's visual storytelling.

    2. **Highly Detailed AI Image Prompts**:
    - Generate **cinematically immersive and hyper-detailed AI prompts** for each segment.
    - Ensure descriptions include **specific settings, character emotions, weather conditions, lighting, background details, clothing styles, and artistic themes**.
    - Use **vivid sensory details** to enhance realism (e.g., "soft raindrops trickling down a foggy window, distant neon lights reflecting on wet pavement").

    3. **Timing Estimation**:
    - Estimate the **optimal duration** each generated image should appear based on the song’s pacing and mood shifts.

    4. **Advanced Video Enhancements**:
    - **Transitions**: Choose the best cinematic transitions like **fade-in, glitch, cross dissolve, zoom cuts, whip pan, VHS distortion, light leaks**.
    - **Lighting & Color Grading**: Apply effects like **soft glow, cyberpunk hues, golden-hour warmth, misty noir tones, dramatic chiaroscuro**.
    - **Camera Movements**: Suggest **cinematic zoom-ins, slow pans, tracking shots, parallax shifts, aerial views, handheld shaky cam**.
    - **VFX (Visual Effects)**: Add dynamic elements such as **smoke, mist, embers, fireflies, falling petals, rain, animated glitch distortions, floating particles**.

    5. **Emotion & Theme Matching**:
    - Ensure that the generated visuals and effects **enhance the emotional intensity, energy, and storytelling depth** of the lyrics.
    - **Each scene should feel alive, expressive, and emotionally immersive**.

    ---


    ### **Output Format:**
    Your response should be a structured list, where each entry contains:
    IMPORTANT: ensure output is properly json formatted as i specified.

    **Format:**  
    ```json[[image_prompt_1, duration, transition_effect, lighting_style, camera_movement, VFX_effects][image_prompt_2, ...]...]```

    Each element corresponds to:
    - `image_prompt`: **Highly detailed AI prompt describing the scene.**
    - `duration`: **Seconds the image should appear in the video.**
    - `transition_effect`: **Cinematic transition effect between scenes.**
    - `lighting_style`: **Visual tone (e.g., warm golden hour, cyberpunk neon, misty noir, soft moonlight).**
    - `camera_movement`: **Dynamic motion of the scene (e.g., slow pan, zoom-in, parallax, handheld).**
    - `VFX_effects`: **Visual enhancements (e.g., fog, fireflies, glowing embers, dust particles, rain, glitch distortions).**

    ---
    ## **Example Output**
    ```json
    [
        [
            "A lonely man in a dimly lit café, gazing out at the rain-soaked streets. His reflection is faintly visible in the glass, neon lights flickering in the background, evoking a sense of longing.", 
            3.0, 
            "Slow fade-in", 
            "Cinematic warm glow with soft shadows", 
            "Slow zoom-in on the man's face", 
            "Raindrop overlay on window, slight mist effect"
        ],
        [
            "A woman walking alone down a foggy street at midnight, street lamps casting long shadows, her silhouette framed against the distant glow of car headlights.", 
            3.5, 
            "Cross dissolve to create a dreamy transition", 
            "Cool blue and purple hues with a misty noir effect", 
            "Tracking shot following her footsteps", 
            "Soft drifting fog, subtle falling raindrops"
        ],
        [
            "A shattered glass heart floating in a surreal, dreamlike space. Cracks spreading as each raindrop touches it, symbolizing heartbreak and time passing.", 
            2.5, 
            "Fast glitch transition", 
            "Ethereal lighting with a deep blue glow", 
            "Dynamic 360-degree rotation around the heart", 
            "Shattering glass effect with glowing fragments dispersing"
        ],
        [
            "An empty park bench under a streetlight, leaves gently falling, a distant figure walking away, symbolizing loss and solitude.", 
            4.0, 
            "Soft dissolve to emphasize emotional weight", 
            "Muted autumn tones with golden highlights", 
            "Slow pan from the bench to the distant figure", 
            "Falling autumn leaves, subtle fog effect"
        ],
        [
            "A sunrise over a vast city skyline, golden rays breaking through the clouds, symbolizing hope and a new beginning.", 
            5.0, 
            "Warm fade-in to signify transition to hope", 
            "Soft golden-hour glow with a dreamy haze", 
            "Aerial zoom-out, revealing the full cityscape", 
            "Lens flare, soft mist, light breeze effect"
        ]
    ]
    ```
    """

    prompt = f"{system_instruction}\n\nUser: {user_input}"
    response = model.generate_content(prompt)
    md_text = response.candidates[0].content.parts[0].text
    # plaintext = clean_markdown(md_text)
    validJson = remove_code_block_markers(md_text)
    return validJson

# # Example Usage
# user_input = "Generate image prompts and video effects for a melancholic song about lost love."
# ans = imgPrompt(user_input)
# print(ans)
