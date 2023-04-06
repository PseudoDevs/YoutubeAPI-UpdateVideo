import os
import pickle
import json
import time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timezone

client_secret_file = "client_secret.json"
video_id = "oqJuhTJwxBA" # changing the video_id for checking
sleep_time = 600  # 10 minutes


def get_credentials():
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            client_secret_file, scopes=["https://www.googleapis.com/auth/youtube"]
        )
        credentials = flow.run_local_server(
            port=8080, prompt="consent", authorization_prompt_message=""
        )
        with open("token.pickle", "wb") as f:
            pickle.dump(credentials, f)
    return credentials


def edit_title(views, youtube):
    video_response = youtube.videos().list(id=video_id, part="snippet").execute()
    video_snippet = video_response["items"][0]["snippet"]
    video_snippet["title"] = f"view_count: {views}"

    youtube.videos().update(
        part="snippet",
        body=dict(snippet=video_snippet, id=video_id)
    ).execute()

    with open("execute_logs.txt", "a") as f:
        f.write(f"{datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')}\n")

    time.sleep(sleep_time)
    get_views()


def get_views():
    youtube = build("youtube", "v3", credentials=get_credentials())
    response = youtube.videos().list(part="statistics", id=video_id).execute()
    views = response["items"][0]["statistics"]["viewCount"]
    print(views)
    edit_title(views, youtube)


while True:
    get_views()
