import os, pickle, json, time
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from datetime import datetime, timezone

client_secret_file = "client_secret.json"

credentials = None

def edit_title(views, credentials):
    youtube = build("youtube", "v3", credentials=credentials)

    video_response = youtube.videos().list(
        id = "cufr0J9D3aI",
        part = "snippet"
    ).execute()

    video_snippet = video_response["items"][0]["snippet"]

    video_snippet['title'] = "view_count: " + str(views)

    youtube.videos().update(
        part    = "snippet",
        body    = dict(
            snippet = video_snippet,
            id = "cufr0J9D3aI"
        )
    ).execute()

    utc_dt = datetime.now(timezone.utc)
    dt = str(utc_dt.astimezone())
    date_time = dt.split('.')[0]

    f = open("execute_logs.txt", "a")
    f.write(date_time+"\n")
    f.close()

    time.sleep(600) # 10 mins
    main_exec()

def get_views(credentials):
    youtube = build("youtube", "v3", credentials=credentials)

    request = youtube.videos().list(
        part = "statistics",
        id   = "cufr0J9D3aI"
    )

    response = request.execute()
    fix_response = str(response).replace("'", '"')
    parsed_response = json.loads(fix_response)

    views = parsed_response["items"][0]["statistics"]["viewCount"]
    print(views) # 23
    edit_title(views, credentials)

def main_exec():
    if os.path.exists('token.pickle'):
        print('true')
    with open('token.pickle', 'rb') as token:
        credentials = pickle.load(token)
    get_views(credentials)

    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('refresh')
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secret_file,
                scopes=[
                    'https://www.googleapis.com/auth/youtube',
                ]
            )

            flow.run_local_server(port=8080, prompt='consent', authorization_prompt_message='')
            credentials = flow.credentials

            # Save the credentials for the next run
            with open('token.pickle', 'wb') as f:
                print('save')
                pickle.dump(credentials, f)

while True:
    main_exec()
