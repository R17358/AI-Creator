
import requests
import os
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("BG_REMOVER_API_URL")
API_KEY = os.getenv("BG_REMOVER_API_KEY")

  # Replace with your actual API key
  
IMAGE_PATH = "sample_test/durga ma.jpg"       # Replace with your image path
OUTPUT_PATH = "output.png"      # Output transparent PNG

# Open image file
with open(IMAGE_PATH, "rb") as image_file:
    response = requests.post(
        API_URL,
        files={"image_file": image_file},
        data={"size": "auto"},
        headers={"X-Api-Key": API_KEY},
    )

# Save output if successful
if response.status_code == 200:
    with open(OUTPUT_PATH, "wb") as out_file:
        out_file.write(response.content)
    print("Background removed successfully! Saved as", OUTPUT_PATH)
else:
    print("Error:", response.text)
