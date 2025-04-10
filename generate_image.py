import os
from google import genai
from google.genai import types
from PIL import Image
from io import BytesIO
import time
import random

# Configure the API key from environment variable
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY environment variable is not set")

# Initialize the client
client = genai.Client(api_key=api_key)

# Define the prompt for image generation
prompt = "Generate a story about a cute baby turtle in a 3d digital art style. For each scene, generate an image."

print(f"Sending request to generate image with prompt: {prompt}")

# Function to implement retry with exponential backoff
def retry_with_backoff(func, max_retries=5, initial_delay=2):
    retries = 0
    while retries < max_retries:
        try:
            return func()
        except Exception as e:
            retries += 1
            if retries == max_retries:
                raise
            delay = initial_delay * (2 ** (retries - 1)) + random.uniform(0, 1)
            print(f"Request failed: {e}. Retrying in {delay:.2f} seconds (attempt {retries}/{max_retries})")
            time.sleep(delay)

# Create a directory for the images (even if we fail, we'll need this for the workflow)
os.makedirs('turtle_images', exist_ok=True)
    
# Generate backup content if API fails completely
def create_backup_content():
    print("API request failed too many times. Creating backup content...")
    
    # Write a simple story
    story = """# The Adventures of Tiny the Turtle

Once upon a time, there was a small baby turtle named Tiny. 
He had a beautiful green shell and curious eyes that sparkled in the sunlight.

Tiny loved exploring the sandy beach where he was born. 
Each day was a new adventure for the little turtle.

One day, Tiny found his way to the ocean and began his journey into the big blue sea.

The waves carried him gently as he discovered a wonderful underwater world full of colorful fish and plants.

Tiny grew stronger every day and knew that one day he would return to the same beach to start a family of his own.

The End."""
    
    with open('output_story.txt', 'w') as f:
        f.write(story)
    print("Backup story created and saved to output_story.txt")
    
    # Create a simple turtle image
    img = Image.new('RGB', (800, 600), color=(0, 105, 148))
    from PIL import ImageDraw
    draw = ImageDraw.Draw(img)
    
    # Draw a simple turtle shape (shell)
    draw.ellipse((300, 200, 500, 400), fill=(34, 139, 34), outline=(0, 100, 0), width=3)
    
    # Head
    draw.ellipse((470, 270, 530, 330), fill=(34, 139, 34), outline=(0, 100, 0), width=3)
    
    # Eyes
    draw.ellipse((490, 280, 500, 290), fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    draw.ellipse((510, 280, 520, 290), fill=(255, 255, 255), outline=(0, 0, 0), width=1)
    
    # Shell pattern
    for i in range(3):
        draw.ellipse((320 + i*30, 220 + i*30, 480 - i*30, 380 - i*30), outline=(0, 80, 0), width=2)
    
    # Text
    draw.text((50, 50), "Tiny the Turtle", fill=(255, 255, 0))
    draw.text((50, 80), "(Backup image - API was unavailable)", fill=(255, 255, 255))
    
    # Save images
    img.save('output_image.png')
    img.save('turtle_images/image_1.png')
    print("Backup image created and saved")

try:
    # Wrap the API call in our retry function
    def generate_content_with_retry():
        return client.models.generate_content(
            model="gemini-2.0-flash-exp-image-generation",
            contents=[prompt],
            config=types.GenerateContentConfig(
                response_modalities=["Text", "Image"]
            ),
        )
    
    # Execute API call with retry
    print("Attempting to generate content with retries...")
    response = retry_with_backoff(generate_content_with_retry)
    
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
    print(f"Error after all retries: {e}")
    # Generate backup content if all retries fail
    create_backup_content()
