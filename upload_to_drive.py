import os
import io
import requests
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.auth.transport.requests import Request

def download_google_drive_file(file_id, destination):
    """
    Download a file from Google Drive by its ID
    """
    URL = "https://docs.google.com/uc?export=download"
    
    session = requests.Session()
    response = session.get(URL, params={'id': file_id}, stream=True)
    token = None
    
    for key, value in response.cookies.items():
        if key.startswith('download_warning'):
            token = value
    
    if token:
        response = session.get(URL, params={'id': file_id, 'confirm': token}, stream=True)
    
    with open(destination, 'wb') as f:
        for chunk in response.iter_content(chunk_size=32768):
            if chunk:
                f.write(chunk)
    
    return destination

def extract_file_id_from_url(url):
    """
    Extract the file ID from a Google Drive URL
    """
    # Expected format: https://drive.google.com/file/d/FILE_ID/view
    if '/file/d/' in url:
        start = url.find('/file/d/') + 8
        end = url.find('/', start)
        return url[start:end]
    return None

def upload_to_drive(credentials_path, file_path, folder_id=None):
    """
    Upload a file to Google Drive
    """
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, 
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    # Build the Drive service
    service = build('drive', 'v3', credentials=credentials)
    
    # File metadata
    file_name = os.path.basename(file_path)
    file_metadata = {'name': file_name}
    
    # If folder_id is provided, set the parent folder
    if folder_id:
        file_metadata['parents'] = [folder_id]
    
    # Upload file
    media = MediaFileUpload(file_path, resumable=True)
    file = service.files().create(body=file_metadata,
                                  media_body=media,
                                  fields='id').execute()
    
    print(f'File {file_name} uploaded to Google Drive with ID: {file["id"]}')
    return file['id']

def upload_directory_to_drive(credentials_path, directory_path, folder_name=None):
    """
    Upload an entire directory to Google Drive
    """
    # Load credentials
    credentials = service_account.Credentials.from_service_account_file(
        credentials_path, 
        scopes=['https://www.googleapis.com/auth/drive']
    )
    
    # Build the Drive service
    service = build('drive', 'v3', credentials=credentials)
    
    # Create a folder if folder_name is provided
    parent_folder_id = None
    if folder_name:
        folder_metadata = {
            'name': folder_name,
            'mimeType': 'application/vnd.google-apps.folder'
        }
        folder = service.files().create(body=folder_metadata, fields='id').execute()
        parent_folder_id = folder['id']
        print(f'Created folder: {folder_name} with ID: {parent_folder_id}')
    
    # Upload all files in the directory
    uploaded_files = []
    for filename in os.listdir(directory_path):
        file_path = os.path.join(directory_path, filename)
        if os.path.isfile(file_path):
            file_metadata = {'name': filename}
            if parent_folder_id:
                file_metadata['parents'] = [parent_folder_id]
            
            media = MediaFileUpload(file_path, resumable=True)
            file = service.files().create(body=file_metadata,
                                        media_body=media,
                                        fields='id').execute()
            
            print(f'File {filename} uploaded with ID: {file["id"]}')
            uploaded_files.append({'name': filename, 'id': file['id']})
    
    return {
        'folder_id': parent_folder_id,
        'files': uploaded_files
    }

def main():
    # Get credentials file URL from command line
    credentials_url = "https://drive.google.com/file/d/152LtocR_Lvll37IW3GXJWAowLS02YBF2/view?usp=sharing"
    
    # Extract Google Drive file ID
    file_id = extract_file_id_from_url(credentials_url)
    
    if not file_id:
        print("Error: Could not extract file ID from URL")
        return
    
    # Download credentials file
    print(f"Downloading credentials file with ID: {file_id}")
    credentials_path = "credentials.json"
    download_google_drive_file(file_id, credentials_path)
    
    # Upload turtle_images directory
    if os.path.exists('turtle_images'):
        print("Uploading turtle_images directory to Google Drive")
        result = upload_directory_to_drive(
            credentials_path,
            'turtle_images',
            folder_name='Gemini Generated Turtle Images'
        )
        
        print(f"\nAll images were uploaded to Google Drive folder with ID: {result['folder_id']}")
        print(f"Direct link to folder: https://drive.google.com/drive/folders/{result['folder_id']}")
        
        # Write the drive links to a file
        with open('drive_links.txt', 'w') as f:
            f.write(f"Google Drive Folder: https://drive.google.com/drive/folders/{result['folder_id']}\n\n")
            f.write("Individual files:\n")
            for file in result['files']:
                f.write(f"{file['name']}: https://drive.google.com/file/d/{file['id']}/view\n")
    else:
        print("turtle_images directory not found")
    
    # Upload story file if it exists
    if os.path.exists('output_story.txt'):
        print("\nUploading story file to Google Drive")
        file_id = upload_to_drive(credentials_path, 'output_story.txt')
        print(f"Story uploaded to: https://drive.google.com/file/d/{file_id}/view")
        
        # Add to drive links file
        with open('drive_links.txt', 'a') as f:
            f.write(f"\nStory file: https://drive.google.com/file/d/{file_id}/view\n")
    
    print("\nAll uploads completed. Links saved to drive_links.txt")

if __name__ == "__main__":
    main()
