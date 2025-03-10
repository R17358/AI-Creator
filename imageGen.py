# import streamlit as st
import requests
import io
from PIL import Image
import numpy as np
import time
import cv2
import os
from dotenv import load_dotenv

load_dotenv()

# API_URL = os.getenv("otherImg_url")
API_KEY = os.getenv("HUGGINGFACE_KEY")
API_URL = "https://api-inference.huggingface.co/models/black-forest-labs/FLUX.1-schnell"

headers = {"Authorization": f"Bearer {API_KEY}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        return response.content
    except requests.exceptions.JSONDecodeError:
        return {"error": "Response could not be decoded as JSON"}

def ImageGenerator(prompt):
    try:
        output = query({"inputs": prompt})
        image = Image.open(io.BytesIO(output))
        os.makedirs("Generated_Images", exist_ok=True)
        filename = os.path.join("Generated_Images", f"image_{int(time.time())}.jpg")
        image.save(filename)
        # image.show()
        return image, filename
    except Exception as e:
        print(e)
        return None, str(e)

# st.title("Image Generator")

# prompt = input("Enter prompt:")

# ans = ImageGenerator(prompt)
# if st.button("Generate Image"):
#     if prompt:
#         image, filename = ImageGenerator(prompt)
#         st.image(image, caption=f"Generated Image ({filename})", use_column_width=True)
#         st.write(f"Image saved as {filename}")
#     else:
#         st.warning("Please enter a prompt.")
