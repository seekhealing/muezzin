import pickle
import os.path

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = [
    'https://www.googleapis.com/auth/gmail.send',
    'https://www.googleapis.com/auth/calendar.readonly',
    'https://www.googleapis.com/auth/spreadsheets.readonly'
]

PICKLE_PATH = os.path.join('muezzin', 'token.pickle')

creds = None
if os.path.exists(PICKLE_PATH):
    with open(PICKLE_PATH, 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join('muezzin', 'credentials.json'), SCOPES)
        creds = flow.run_local_server()
    # Save the credentials for the next run
    with open(PICKLE_PATH, 'wb') as token:
        pickle.dump(creds, token)