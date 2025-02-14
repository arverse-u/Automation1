import os
import pickle
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

TOKEN_FILE = 'token_youtube.pickle'

# Load YouTube API client

def get_authenticated_service():
    with open(TOKEN_FILE, 'rb') as token:
        credentials = pickle.load(token)
    return build('youtube', 'v3', credentials=credentials)

def upload_video(video_path, title, description, tags, privacy_status='public'):
    youtube = get_authenticated_service()

    request_body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': '27',  # education
        },
        'status': {
            'privacyStatus': privacy_status,  # Options: 'public', 'private', 'unlisted'
        }
    }

    media = MediaFileUpload(video_path, chunksize=-1, resumable=True, mimetype='video/*')

    try:
        upload_request = youtube.videos().insert(
            part='snippet,status',
            body=request_body,
            media_body=media
        )

        response = upload_request.execute()
        print(f"✅ Video uploaded successfully: https://www.youtube.com/watch?v={response['id']}")
        return response['id']

    except HttpError as e:
        print(f"❌ An HTTP error occurred: {e.resp.status} - {e.content}")
        return None

if __name__ == '__main__':
    video_path = 'buffer/test1.mp4'
    title = 'Sample Quiz Title #shorts'
    description = 'Sample quiz description with options and call-to-action.'
    tags = ['quiz', 'learning', 'shorts', 'education', 'knowledge']

    upload_video(video_path, title, description, tags)
