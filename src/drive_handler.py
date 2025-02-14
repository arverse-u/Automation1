import os
import io
import pickle
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow # type: ignore
from google.oauth2.credentials import Credentials
from src.config import DRIVE_FOLDER_ID, BUFFER_FOLDER

# Scopes required for Google Drive API access
SCOPES = ['https://www.googleapis.com/auth/drive']


def get_drive_service():
    """Authenticate and return the Google Drive service."""
    creds = None

    # Load existing token from token_drive.pickle
    if os.path.exists('token_drive.pickle'):
        with open('token_drive.pickle', 'rb') as token_file:
            creds = pickle.load(token_file)

    # If token is not available or invalid, start authentication flow
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        # Save the new token as token_drive.pickle
        with open('token_drive.pickle', 'wb') as token_file:
            pickle.dump(creds, token_file)

    return build('drive', 'v3', credentials=creds)


def fetch_oldest_video():
    """Fetch the oldest video from the Google Drive folder and download it to the buffer folder."""
    drive_service = get_drive_service()

    # Fetch files from the folder
    results = drive_service.files().list(
        q=f"'{DRIVE_FOLDER_ID}' in parents and mimeType contains 'video/' and trashed=false",
        fields="files(id, name, createdTime)",
        orderBy="createdTime"
    ).execute()

    files = results.get('files', [])

    if not files:
        print("No videos found in the folder.")
        return None

    # Oldest video (first file in the sorted list)
    oldest_file = files[0]
    file_id = oldest_file['id']
    file_name = oldest_file['name']

    # Ensure buffer folder exists
    os.makedirs(BUFFER_FOLDER, exist_ok=True)

    video_path = os.path.join(BUFFER_FOLDER, file_name)

    # Download video
    request = drive_service.files().get_media(fileId=file_id)
    fh = io.FileIO(video_path, 'wb')
    downloader = MediaIoBaseDownload(fh, request)

    print(f"Downloading video: {file_name}...")

    done = False
    while not done:
        status, done = downloader.next_chunk()
        print(f"Download {int(status.progress() * 100)}%.")

    print(f"Video downloaded to: {video_path}")

    return video_path, file_id


def delete_video_from_drive(file_id):
    """Delete a video from Google Drive by file ID."""
    drive_service = get_drive_service()
    drive_service.files().delete(fileId=file_id).execute()
    print(f"Deleted video from Drive (File ID: {file_id})")


# Optional: For testing this module independently
if __name__ == "__main__":
    video_path, file_id = fetch_oldest_video()
    print(f"Video Path: {video_path}, Drive File ID: {file_id}")
