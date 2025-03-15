
# AI Creator

##Add .env file:
  
  IMG_API_URL = https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell
  
  HUGGINGFACE_KEY =
  
  GEMINI_API_KEY = 
  
  IMG_TO_TEXT_URL=https://api-inference.huggingface.co/models/Salesforce/blip-image-captioning-large
  
  BG_REMOVER_API_KEY=
  BG_REMOVER_API_URL=https://api.remove.bg/v1.0/removebg
  
  IMG_API_KEY_DREAMSHAPER =
  IMG_API_URL_DREAMSHAPER = https://api.segmind.com/v1/sdxl1.0-dreamshaper


## Overview
**AI Creator** is a Python and Streamlit-based web application designed to simplify video creation for social media platforms like YouTube and Instagram. By providing a prompt, users can generate an entire video with AI-generated music, lyrics, and visuals, making content creation effortless.

## Features
- **AI-Powered Prompt Enhancement:** Enhances the user's video idea prompt to generate more engaging content.
- **AI-Generated Lyrics:** Generates song lyrics based on the provided prompt.
- **AI Music & Singing:** Uses Suno AI to create music and vocals.
- **AI Image Generation:** Generates multiple images according to the lyrics using AI.
- **Automatic Video Compilation:** Combines images with appropriate transitions and effects.
- **Text-to-JSON Formatting:** Uses `gemini-1.5-flash` to output structured JSON data, defining:
  - Image prompts
  - Transition types
  - Image durations
  - VFX effects
- **Landscape & Portrait Video Options:** Supports both aspect ratios for different platforms.
- **Video Editing Libraries:** Utilizes `ffmpeg` and `moviepy` for efficient video processing.

## Technologies Used
- **Python** & **Streamlit** (for web-based UI)
- **Google Gemini-1.5-Flash** (for text and structured JSON generation)
- **Suno AI** (for music and singing)
- **FFmpeg & MoviePy** (for video editing and rendering)
- **Various AI Libraries** for image generation and effects

## How It Works
1. **User Input:** Enter a prompt describing the desired video theme.
2. **AI Processing:**
   - Enhances the prompt.
   - Generates song lyrics.
   - Creates a song using Suno AI.
   - Produces images based on lyrics.
   - Structures transitions, durations, and effects in JSON format.
3. **Video Generation:**
   - Images are compiled into a video with transitions and effects.
   - The AI-generated song is added as background music.
   - The final video is rendered in landscape or portrait mode.
4. **Output:** Download the completed video for social media sharing.

## Installation
```sh
# Clone the repository
git clone https://github.com/R17358/AI-Creator.git
cd ai-creator

# Install dependencies
pip install -r requirements.txt

# Run the Streamlit app
streamlit run app.py
```

## Usage
1. Run the application using `streamlit run app.py`.
2. Enter a video prompt.
3. Let the AI generate lyrics, music, images, and compile the video.
4. Download and share your AI-generated video!

## Future Enhancements
- Support for more AI models for text and image generation.
- Advanced customization options for video editing.
- Integration with social media APIs for direct uploading.

## Contributing
Contributions are welcome! Feel free to fork the repository, create a new branch, and submit a pull request.

## License
This project is licensed under the MIT License.

