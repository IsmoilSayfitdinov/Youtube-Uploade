from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow
from django.conf import settings

# YouTube API konfiguratsiyalari
CLIENT_SECRETS_FILE = "client_secrets.json"
YOUTUBE_UPLOAD_SCOPE = ["https://www.googleapis.com/auth/youtube.upload"]
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"


def upload_to_youtube(video):
    flow = InstalledAppFlow.from_client_secrets_file(
        CLIENT_SECRETS_FILE, scopes=YOUTUBE_UPLOAD_SCOPE)
    credentials = flow.run_local_server(port=0)  # Autentifikatsiya uchun lokal serverni ishga tushirish

    # YouTube API bilan ishlash uchun klient yaratish
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=credentials)

    body = {
        'snippet': {
            'title': video.title,
            'description': video.description,
            'tags': ['tag1', 'tag2'],
            'categoryId': video.category
        },
        'status': {
            'privacyStatus': video.privacy_status
        }
    }
    media_body = MediaFileUpload(video.video_file.path, chunksize=-1, resumable=True)
    insert_request = youtube.videos().insert(
        part=",".join(body.keys()),
        body=body,
        media_body=media_body
    )

    response = None
    while response is None:
        status, response = insert_request.next_chunk()

    if 'id' in response:
        return response['id']
    else:
        raise Exception("The upload failed with an unexpected response.")