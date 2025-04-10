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
    
    # Create a directory for the images
    os.makedirs('turtle_images', exist_ok=True)
    
    # Variables to track images and story
    full_story = ""
    image_count = 0
    
    # Process the response and save the generated images with unique filenames
    for part in response.candidates[0].content.parts:
        if hasattr(part, 'text') and part.text is not None:
            print(part.text)
            full_story += part.text + "\n"
            
        elif hasattr(part, 'inline_data') and part.inline_data is not None:
            image_count += 1
            image_filename = f'turtle_images/image_{image_count}.png'
            print(f"Saving image {image_count}...")
            image = Image.open(BytesIO(part.inline_data.data))
            image.save(image_filename)
            print(f"Image saved as {image_filename}")
            
            # Also save the latest image as output_image.png for compatibility
            image.save('output_image.png')
    
    # Save the complete story
    with open('output_story.txt', 'w') as f:
        f.write(full_story)
    print(f"Story saved to output_story.txt")
    print(f"Generated {image_count} images in the 'turtle_images' folder")
        
except Exception as e:
    print(f"Error: {e}")
