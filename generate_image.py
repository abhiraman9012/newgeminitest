import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Configure the API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

# Initialize the client
client = genai.Client(api_key=api_key)

# Define the prompt for image generation
prompt = "Generate a story about a cute baby turtle in a 3d digital art style. For each scene, generate an image."

print(f"Sending request to generate image with prompt: {prompt}")

# Generate content with text and image modalities
try:
    response = client.models.generate_content(
        model="gemini-2.0-flash-exp-image-generation",
        contents=[prompt],
        config=types.GenerateContentConfig(
            response_modalities=["Text", "Image"]
        ),
    )
    
    # Process the response and save the generated image
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text') and part.text is not None:
            print(part.text)
            # Save text to a file
            with open('output_story.txt', 'w') as f:
                f.write(part.text)
        elif hasattr(part, 'inline_data') and part.inline_data is not None:
            print("Saving image...")
            image = Image.open(BytesIO(part.inline_data.data))
            image.save('output_image.png')
            print("Image saved as output_image.png")
        
except Exception as e:
    print(f"Error: {e}")
