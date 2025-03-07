import requests
import io
from PIL import Image
import time
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("IMG_API_KEY_DREAMSHAPER")
url = os.getenv("IMG_API_URL_DREAMSHAPER")

def ImageGenerator(prompt, width=1024, height=1024):
    # Request payload
    data = {
    "prompt": f"{prompt}",
    # "negative_prompt": "drawing, painting, crayon, sketch, graphite, impressionist, noisy, blurry, soft, deformed, ugly, [deformed | disfigured], poorly drawn, [bad : wrong] anatomy, [extra | missing | floating | disconnected] limb, (mutated hands and fingers), blurry",
    "samples": 1,
    "scheduler": "UniPC",
    "num_inference_steps": 35,
    "guidance_scale": "7",
    "seed": "1135424276",
    "img_width": f"{width}",
    "img_height": f"{height}",
    "base64": False
    }

    try:
        
        response = requests.post(url, json=data, headers={'x-api-key': api_key})

        print(f"Status Code: {response.status_code}")
        # print(f"Response Headers: {response.headers}")
        # print(f"Response Content: {response.content}")

        if response.status_code == 200:
            image_bytes = response.content
            if not image_bytes or b"error" in image_bytes.lower():
                return None, "Error in fetching image"
            # Convert to an image
            image = Image.open(io.BytesIO(image_bytes))
            os.makedirs("Generated_Images", exist_ok=True)

            filename = os.path.join("Generated_Images", f"image_{int(time.time())}.jpg")
            image.save(filename)

            # # Show the image
            # image.show()
        
        
        return image, filename
    except Exception as e:
        print(e)
        return None, str(e)
    
# prompt = "A semirealistic eagle flying in the sky"
# val, file = ImageGenerator(prompt)
# print(val)
# print(file)
