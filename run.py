#pip install google-api-python-client
#pip install google-auth-httplib2
#pip install google-auth-oauthlib
#srcs:
#https://developers.google.com/calendar/quickstart/python
#https://developers.google.com/calendar
#follow steps to: Enable the Google Calendar API
#download client configuration and copy to active folder


from __future__ import print_function
import datetime
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

from random import randint
import time

#if scopes modfied, delete `token.json`
scopes = ['https://www.googleapis.com/auth/calendar']

creds = None
if os.path.exists('token.json'):
    creds = Credentials.from_authorized_user_file('token.json')
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', scopes)
        creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

service = build('calendar', 'v3', credentials=creds)

now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
print('Getting events...')
events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                    orderBy='startTime').execute()
events = events_result.get('items', [])
#print(events)

while True:
    for event in events:
        summary = event.get('summary', None)
        if summary == 'test':
            start = event['start']['dateTime']
            end = event['start']['dateTime']
            #https://lukeboyle.com/blog-posts/2016/04/google-calendar-api---color-id
            newColor = randint(0, 11)
            event['colorId'] = newColor
            #print(event['colorId'])
            #https://developers.google.com/calendar/v3/reference/events/update
            service.events().update(calendarId='primary', eventId=event['id'], sendNotifications=False, body=event).execute()
    time.sleep(.5)

























