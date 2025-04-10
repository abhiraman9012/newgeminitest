import os
from google import genai
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

# Generate content with image modality
try:
    response = client.models.generate_images(
        model="imagen-3.0-generate-002",
        prompt=prompt,
        config=genai.types.GenerateImagesConfig(
            number_of_images=1,
            output_mime_type="image/png",
        ),
    )
    
    # Save the generated image
    if response.generated_images:
        image = response.generated_images[0].image
        image.save('output_image.png')
        print("Image saved successfully to output_image.png")
    else:
        print("No images were generated in the response")
        
except Exception as e:
    print(f"Error generating image: {e}")
