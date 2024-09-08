from gradio_client import Client
import requests
import os

def generate_img(prompt):
    client = Client("ByteDance/Hyper-FLUX-8Steps-LoRA")
    result = client.predict(
        height=1024,
		width=1024,
		steps=8,
		scales=3.5,
		prompt=prompt,
		seed=3413,
		api_name="/process_image"
    )

    
    image_url = result  # Adjust this if the URL is nested within the result

    # Check if the URL is a local file path
    if os.path.isfile(image_url):
        with open(image_url, "rb") as file:
            content = file.read()
        with open("output_filename.png", "wb") as file:
            file.write(content)
        
    else:
        # Download the image from the web URL
        response = requests.get(image_url)
        if response.status_code == 200:
            with open("output_filename.png", "wb") as file:
                file.write(response.content)
            
        else:
            print("Failed to download image")
            return
        return

# Example usage
generate_img(prompt="Shrek in a forest")