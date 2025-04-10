import os
import google.generativeai as genai
from PIL import Image
from io import BytesIO

# Configure the API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Define the prompt for image generation
prompt = "Generate a story about a cute baby turtle in a 3d digital art style. For each scene, generate an image."

# Generate content with text and image modalities
model = genai.GenerativeModel('gemini-2.0-flash-exp-image-generation')

response = model.generate_content(
    contents=[prompt],
    generation_config={
        "response_mime_types": ["text/plain", "image/png"]
    }
)

# Process the response and save the generated image
print("Response received from Gemini API")
for part in response.candidates[0].content.parts:
    if hasattr(part, 'text') and part.text is not None:
        print(part.text)
    elif hasattr(part, 'inline_data') and part.inline_data is not None:
        print("Saving image...")
        image = Image.open(BytesIO(part.inline_data.data))
        image.save('output_image.png')
        print("Image saved as output_image.png")
