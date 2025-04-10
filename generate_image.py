from PIL import Image, ImageDraw, ImageFont
import datetime

# Create a new image with white background
image = Image.new('RGB', (800, 600), (255, 255, 255))
draw = ImageDraw.Draw(image)

# Draw a sample text
text = "Hello from Gemini API Demo\nPlaceholder Image"
# Use default font
draw.text((50, 50), text, fill=(0, 0, 0))

# Draw a turtle-like shape
# Body (circle)
draw.ellipse((300, 250, 500, 450), fill=(0, 150, 0), outline=(0, 0, 0))
# Head
draw.ellipse((450, 300, 550, 400), fill=(0, 150, 0), outline=(0, 0, 0))
# Eyes
draw.ellipse((490, 330, 510, 350), fill=(255, 255, 255), outline=(0, 0, 0))
draw.ellipse((500, 330, 520, 350), fill=(255, 255, 255), outline=(0, 0, 0))
# Legs
draw.ellipse((290, 300, 340, 350), fill=(0, 150, 0), outline=(0, 0, 0))  # Front left
draw.ellipse((290, 350, 340, 400), fill=(0, 150, 0), outline=(0, 0, 0))  # Back left
draw.ellipse((460, 300, 510, 350), fill=(0, 150, 0), outline=(0, 0, 0))  # Front right
draw.ellipse((460, 350, 510, 400), fill=(0, 150, 0), outline=(0, 0, 0))  # Back right

# Add timestamp
timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
draw.text((50, 550), f"Generated at: {timestamp}", fill=(100, 100, 100))

# Save the image
image.save('output_image.png')
print("Image saved as output_image.png")
