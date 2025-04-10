import os
import requests
import shutil
from datetime import datetime

def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
    return directory

def download_file(url, destination):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            with open(destination, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Downloaded: {destination}")
            return True
        else:
            print(f"Failed to download {url}. Status code: {response.status_code}")
            return False
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False

def main():
    # Create a timestamped download directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    download_dir = create_directory(f"downloaded_turtle_images_{timestamp}")
    
    # Repository information
    repository = input("Enter your GitHub repository (username/repo): ") or "abhiraman9012/newgeminitest"
    workflow_run_id = input("Enter the workflow run ID (or press Enter to use latest): ") or "latest"
    
    # Number of images to try downloading
    num_images = int(input("How many images to download (default 6): ") or "6")
    
    # Base URLs for raw file content on GitHub Actions runner
    run_url = f"https://github.com/{repository}/actions/runs/{workflow_run_id}"
    
    # Create an index.html file to view all the images
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Gemini Generated Turtle Images</title>
        <style>
            body {{ font-family: Arial, sans-serif; max-width: 1200px; margin: 0 auto; padding: 20px; }}
            h1 {{ color: #2a7ae2; }}
            .image-container {{ display: flex; flex-wrap: wrap; gap: 20px; margin-top: 30px; }}
            .image-card {{ border: 1px solid #ddd; border-radius: 8px; overflow: hidden; width: 45%; max-width: 500px; margin-bottom: 20px; box-shadow: 0 4px 8px rgba(0,0,0,0.1); }}
            .image-card img {{ width: 100%; height: auto; display: block; }}
            .image-card .caption {{ padding: 15px; background-color: #f8f9fa; }}
            .story {{ background-color: #f8f9fa; padding: 20px; border-radius: 8px; margin-top: 30px; line-height: 1.6; }}
            code {{ background-color: #f1f1f1; padding: 2px 4px; border-radius: 4px; }}
            .note {{ margin-top: 30px; padding: 15px; background-color: #e8f4f8; border-left: 5px solid #2a7ae2; }}
        </style>
    </head>
    <body>
        <h1>Gemini Generated Turtle Images</h1>
        <p>These images were generated using the Google Gemini AI API on {timestamp}.</p>
        
        <div class="story">
            <h2>The Turtle Story</h2>
            <div id="story-content">Loading story...</div>
        </div>
        
        <h2>Images</h2>
        <div class="image-container">
    """
    
    # Try to download each image
    local_images = []
    
    print(f"\nAttempting to download images to {download_dir}...")
    print("Note: This method can only download files that are already saved locally.")
    print("If this doesn't work, you'll need to run the script locally as described below.\n")
    
    # Try downloading from local turtle_images directory
    if os.path.exists('turtle_images'):
        print("Found local turtle_images directory, copying files...")
        if not os.path.exists(os.path.join(download_dir, 'turtle_images')):
            os.makedirs(os.path.join(download_dir, 'turtle_images'))
        
        for i in range(1, num_images + 1):
            src_path = os.path.join('turtle_images', f'image_{i}.png')
            if os.path.exists(src_path):
                dest_path = os.path.join(download_dir, 'turtle_images', f'image_{i}.png')
                shutil.copy2(src_path, dest_path)
                local_images.append(f'turtle_images/image_{i}.png')
                print(f"Copied: {dest_path}")
                
                # Add to HTML
                html_content += f"""
                <div class="image-card">
                    <img src="turtle_images/image_{i}.png" alt="Turtle Scene {i}">
                    <div class="caption">
                        <h3>Scene {i}</h3>
                        <p>Description: Cute baby turtle scene {i}</p>
                    </div>
                </div>
                """
    
    # Copy story if it exists
    story_content = "No story content available."
    story_path = 'output_story.txt'
    if os.path.exists(story_path):
        with open(story_path, 'r') as f:
            story_content = f.read()
        
        # Save to download directory
        shutil.copy2(story_path, os.path.join(download_dir, 'output_story.txt'))
        print(f"Copied story to {os.path.join(download_dir, 'output_story.txt')}")
    
    # Complete the HTML content
    html_content += f"""
        </div>
        
        <div class="note">
            <h3>How to Run This Script Locally</h3>
            <p>If you want to generate more images, follow these steps:</p>
            <ol>
                <li>Clone the repository: <code>git clone https://github.com/{repository}.git</code></li>
                <li>Create an .env file with your Gemini API key: <code>echo "GEMINI_API_KEY=your_api_key" > .env</code></li>
                <li>Install the required dependencies: <code>pip install google-genai==0.1.0 Pillow</code></li>
                <li>Run the generation script: <code>python generate_image.py</code></li>
            </ol>
            <p>This will create a new set of images in the turtle_images directory.</p>
        </div>
        
        <script>
            // Insert the story content
            document.getElementById('story-content').innerHTML = `<p>${story_content.replace(/\n/g, '</p><p>')}</p>`;
        </script>
    </body>
    </html>
    """
    
    # Save the HTML file
    html_path = os.path.join(download_dir, 'index.html')
    with open(html_path, 'w') as f:
        f.write(html_content)
    print(f"\nCreated HTML viewer at: {html_path}")
    
    # Summary
    print(f"\nDownload Summary:")
    print(f"Successfully saved {len(local_images)} images to {download_dir}")
    print(f"Story saved: {'Yes' if os.path.exists(os.path.join(download_dir, 'output_story.txt')) else 'No'}")
    print(f"\nTo view the images, open the HTML file: {html_path}")
    print("\nIf you need to generate new images, run the generate_image.py script locally as described in the HTML page.")

if __name__ == "__main__":
    main()
