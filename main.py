import streamlit as st
from promptEnhancer import promptEnhacerResponse as pe
from LyricsWriter import lyricsResponse
from imageGenPrompter import imgPrompt
from imageGen import ImageGenerator
from TextGeneration import chatResponse
from imageAttacher import create_video, add_music_to_video
from modifiedImgPrompt import modifiedImgPromptResponse as mipr
import time
import json
from imageAttacher import create_video
from fixVideo import fixVideoToShow as fix
import os
from musicFileLen import get_audio_length

st.title("AI CREATOR")
st.divider()

music_file_path = None

save_folder = 'uploaded_music_files'
os.makedirs(save_folder, exist_ok=True)

def save_uploaded_file(uploaded_file, save_folder):
    file_path = os.path.join(save_folder, uploaded_file.name)
    with open(file_path, 'wb') as f:
        f.write(uploaded_file.getbuffer())
    return file_path

numOfPrompts = 5

sidebar = st.sidebar
sidebar.title("Menu")

musicFile = sidebar.file_uploader("Add Song File...", type=['mp3', 'wav', 'ogg'])
if musicFile is not None:
    music_file_path = save_uploaded_file(musicFile, save_folder)
    st.success(f"File saved at: {music_file_path}")
    musicLength = get_audio_length(music_file_path)

    needPrompts = musicLength/2             # Adjust to generate more images and increase video length
    if needPrompts<=15:
        numOfPrompts = needPrompts
    else:
        numOfPrompts = 15

choice = st.radio("Aspect Ratio", ["Landscape", "Portrait", "Square"])
width = height = 1024
if choice == "Landscape":
    width = 1920
    height = 1080
elif choice == "Portrait":
    width = 1080
    height = 1920

home, about = st.tabs(["Home", "About Us"])

with home:
    user_input = st.text_input("Enter Type of Song/Lyrics you want ....")
    
    if user_input:
        try:
            with st.spinner("Generating prompt..."):
                prompt = pe(user_input)
            
            st.text_area("Generated Prompt", prompt)
            time.sleep(1)
            if prompt:
                with st.spinner("Generating lyrics..."):
                    lyrics = lyricsResponse(prompt)
        
                if lyrics:
                    with open("lyrics.txt", "w", encoding="utf-8") as file:
                        file.write(lyrics)
                    st.text_area("Generated Lyrics",lyrics)

                    time.sleep(3)
                    
                    with st.spinner("Generating image prompts..."):
                        imagePrompts = imgPrompt(lyrics, numOfPrompts)

                    genImagesPaths = []
                    imageDuration = []
                    if imagePrompts:   
                        st.text(imagePrompts)
                        with st.spinner("Generating Images...."):
                            if isinstance(imagePrompts, str):  
                                imagePrompts = json.loads(imagePrompts)

                            for p in imagePrompts:
                                img_prompts = []
                                if len(p) > 5:
                                    img_prompts.extend([p[0], p[3], p[5]])
                                    imageDuration.append(p[1])
                                try:
                                    modified_image_prompt = mipr(img_prompts)
                                    st.text(modified_image_prompt)
                                    img, filename = ImageGenerator(modified_image_prompt, width, height)
                                    genImagesPaths.append(filename)
                                    st.image(img)
                                    st.success("Image Generated")
                                    time.sleep(1)
                                except Exception as e:
                                    print(e)
                                    st.error(e)
                        with st.spinner("Generating Video...."):
                            if not os.path.exists("Generated_video"):
                                os.makedirs("Generated_video")
                            output_path_video = f"Generated_video/output_video.mp4"
                            video_path = create_video(genImagesPaths, output_path_video, 30, imageDuration, 1)
                            st.success(f"Video saved at {video_path}")
                            time.sleep(1)
                            if musicFile:
                                output_path_music = f"Generated_video/output_video_music.mp4"
                                add_music_to_video(video_path,music_file_path,output_path_music)
                                st.success("Video Merged with audio")
                            time.sleep(1)  # Small delay to ensure file is fully written

                        with st.spinner("Loading Video"):
                            input_video = "Generated_video/output_video_music.mp4"
                            output_video = f"Generated_video/output_fixed{int(time.time())}.mp4"
                            video = fix(input_video, output_video)
                            try:
                                st.video(video)
                            except Exception as e:
                                st.error(e)


        
        except Exception as e:
            print(e)
            st.error(e)
                        

                        

