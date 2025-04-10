import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO

# Configure the API key from environment variable
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the client
client = genai.Client()

# Define the prompt for image generation
prompt = "Generate a story about a cute baby turtle in a 3d digital art style. For each scene, generate an image."

# Generate content with text and image modalities
response = client.models.generate_content(
    model="gemini-2.0-flash-exp-image-generation",
    contents=[prompt],
    config=types.GenerateContentConfig(
        response_modalities=["Text", "Image"]
    ),
)

# Process the response and save the generated image
for part in response.candidates[0].content.parts:
    if part.text is not None:
        print(part.text)
    elif part.inline_data is not None:
        image = Image.open(BytesIO(part.inline_data.data))
        image.save('output_image.png')
