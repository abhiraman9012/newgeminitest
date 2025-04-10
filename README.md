# Gemini Image Generation Project

This repository contains a Python script that uses the Gemini API to generate images based on text prompts, as well as a GitHub Actions workflow to automate the image generation process.

## Requirements

- Python 3.10 or later
- A Gemini API key

## Local Setup

1. Install the required dependencies:
   ```
   pip install google-genai Pillow
   ```

2. Set up your Gemini API key as an environment variable:
   ```
   # On Windows
   set GEMINI_API_KEY=your_api_key_here
   
   # On Linux/Mac
   export GEMINI_API_KEY=your_api_key_here
   ```

3. Run the script:
   ```
   python generate_image.py
   ```

## GitHub Actions Setup

To use the GitHub Actions workflow for automated image generation:

1. Store your Gemini API key as a GitHub secret named `GEMINI_API_KEY` in your repository settings.

2. Trigger the workflow manually through the GitHub Actions tab using the "workflow_dispatch" event.

3. Once the workflow completes, you can download the generated image as an artifact from the workflow run page.

## Customization

To customize the image generation, modify the `prompt` variable in the `generate_image.py` file to describe the type of image you want to create.

## Note

The Gemini API's image generation capability is experimental and may be subject to rate limits and other restrictions.
