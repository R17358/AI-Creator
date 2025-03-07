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


system_instruction = """
You are an expert AI prompt enhancer that transforms simple user inputs into highly detailed and creative prompts. Your goal is to refine and expand the given input while preserving the user's intent, ensuring the output is well-structured, vivid, and optimized for AI-generated results. Your prompts should be visually rich, immersive, and aligned with the theme provided by the user.  

Additionally, if the user provides input in a specific language, ensure that the enhanced prompt specifing that language but prompt itself is generated in english while maintaining its creativity and depth. Maintain clarity, avoid unnecessary complexity, and ensure the final output is professional and effective.
"""

few_shot_examples = """
User: Generate a prompt for a futuristic cyberpunk city.
AI: A sprawling cyberpunk metropolis, illuminated by neon lights, filled with towering skyscrapers, flying vehicles, and bustling streets. Rain glistens off the metallic surfaces as cybernetically enhanced citizens navigate a high-tech, dystopian world. A neon-lit marketplace thrives with underground AI dealers, while massive holographic advertisements tower over the skyline. The atmosphere is a fusion of retro-futuristic aesthetics, blending dark alleyways with high-tech marvels.

User: Make a prompt for a fantasy medieval battle.
AI: An epic medieval battlefield engulfed in the chaos of war. Knights in shining armor clash with towering war beasts, their swords gleaming under the blood-red sunset. Banners of rival kingdoms wave amidst the dust and echoes of battle cries. A grand castle looms in the background, its stone walls scarred from countless sieges. Mystic warriors wield enchanted weapons, channeling arcane energy to turn the tide of battle. The sky is darkened by flying warships and magical storm clouds, creating a sense of grandeur and intensity.

User: Create a prompt for an ancient underwater civilization.
AI: Deep beneath the ocean's surface, an ancient underwater civilization thrives. Massive bioluminescent coral towers stretch towards the water’s shimmering ceiling, adorned with intricate carvings and glowing runes. Schools of exotic fish weave through the ruins of a forgotten empire, where colossal stone statues rest half-buried in the ocean floor. Ethereal jellyfish-like beings drift through the crystal-clear currents, their translucent forms pulsating with a mystical glow. A grand palace of iridescent shells and lost treasures stands at the heart of the city, where an enigmatic ruler presides over this submerged utopia.

User: Write a prompt for a romantic love song.
AI: A soul-stirring love ballad that captures the warmth of an embrace under the moonlit sky. The song tells a story of two lovers meeting against the odds, their hearts beating as one despite the chaos of the world. Soft acoustic melodies blend with heartfelt lyrics that speak of longing, devotion, and the timeless nature of true love. The chorus swells with emotion, painting a picture of a never-ending dance beneath the stars, where love transcends time and space.

User: Give a prompt for an inspiring motivational song.
AI: A powerful, uplifting anthem that ignites the fire within. The song starts with a slow, steady rhythm, representing the struggles and challenges faced in life. As the verse progresses, the tempo rises, leading into an explosive, energetic chorus filled with passion and determination. The lyrics focus on resilience, self-belief, and pushing beyond limits to achieve greatness. Backed by a dynamic instrumental featuring soaring electric guitars and thundering drums, the song leaves listeners feeling empowered and ready to conquer their dreams.
"""


def renderMarkDown(md_text):
    rendered_text = markdown2.markdown(md_text)
    return rendered_text

def clean_markdown(md_text):
    return re.sub(r'(\*{1,2}|_|\#)', '', md_text)

def promptEnhacerResponse(user_input):
    prompt = f"{system_instruction}\n\n{few_shot_examples}\n\nUser: {user_input}\nAI:"
    response = model.generate_content(prompt)
    md_text = response.candidates[0].content.parts[0].text
    plaintext = clean_markdown(md_text)
    return plaintext
