from google.oauth2 import service_account
from googleapiclient.discovery import build
from datetime import datetime

SCOPES = ['https://www.googleapis.com/auth/calendar']
creds = service_account.Credentials.from_service_account_file(
    'config/service_account.json',
    scopes=SCOPES
)
service = build('calendar', 'v3', credentials=creds)

# This function takes schedule and inserts events
def create_event(date, time_range, task_name):
    start_time, end_time = time_range.split("-")

    start_datetime = f"{date}T{start_time}:00"
    end_datetime = f"{date}T{end_time}:00"

    event = {
        'summary': task_name,
        'start': {
            'dateTime': start_datetime,
            'timeZone': 'America/Los_Angeles'  # ⚠️ Replace with your time zone
        },
        'end': {
            'dateTime': end_datetime,
            'timeZone': 'America/Los_Angeles'
        }
    }

    created_event = service.events().insert(calendarId='primary', body=event).execute()
    print(f"Created event: {created_event.get('htmlLink')}")
def fetch_upcoming_events():
    events_result = service.events().list(
        calendarId='primary',
        maxResults=10,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])
    return events

