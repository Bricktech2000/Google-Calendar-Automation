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

from dateutil.parser import parse as dtparse

from random import randint
import math
import time
import re

priorityColorIds = [8, 3, 1, 2, 5, 6, 11]
progressRegExp = re.compile(r'(\d*)\%(\d+)$')


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


print('Program Running...')
lastEvents = []
while True:
    try:
        now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
        events_result = service.events().list(calendarId='primary', timeMin=now, singleEvents=True,
                                            orderBy='startTime').execute()
        events = events_result.get('items', [])
        #print(events)
    except Exception as e:
        print('Error Fetching Calendar Data: ', e)
        time.sleep(.5)
        continue

    different = False
    for i in range(len(events)):
        if len(events) != len(lastEvents) \
        or dtparse(events[i]['updated']) - dtparse(lastEvents[i]['updated']) \
         > dtparse('0:00:03.000') - dtparse('0:00:00.000'): #3 sec
            different = True
            break
    if not different:
        time.sleep(2)
        continue
    lastEvents = events
    
    for event in events:
        summary = event.get('summary', '')
        #https://docs.python.org/3/howto/regex.html
        matches = progressRegExp.search(summary)
        if matches is not None:
            total, done = matches.group(1, 2)
            if total == '': total = '100'
            eventProgress = int(done) / int(total)
            eventProgress = max(0, min(1, eventProgress))

            #https://developers.google.com/calendar/quickstart/python
            #https://stackoverflow.com/questions/49889379/google-calendar-api-datetime-format-python
            #https://stackoverflow.com/questions/796008/cant-subtract-offset-naive-and-offset-aware-datetimes
            start = event['start']
            end = event['end']
            start = dtparse(start.get('dateTime', start.get('date'))).replace(tzinfo=None)
            end = dtparse(end.get('dateTime', end.get('date'))).replace(tzinfo=None)
            now = datetime.datetime.utcnow()
            durationProgress = (now - start) / (end - start)
            durationProgress = max(0, min(1, durationProgress))

            #factor = 3 #if the event has no (0%) progress, it will have max priority when 1/3 of its duration is left
            #eventPriority = (1 - eventProgress) * (durationProgress ** .5)
            #eventPriority = (1 - eventProgress) * math.sin((1 - durationProgress) * math.pi / 2) + (1 - durationProgress) * math.sin((1 - eventProgress) * math.pi / 2)

            #the time left (from 0 to 1) is on the X axis
            #the work left (from 0 to 1) is on the Y axis
            #the angle from the X axis (rotating counterclockwise, 1/4 turn) is the priority of the event
            #this way, when the time left is equal to 0, the output will always be 1 (max priority)
            #similarely, when the work left is equal to 0, the output will always be 0 (zero priority)
            #finally, when no time is left and none of the work is left, the output will be 0 (zero priority)
            eventPriority = math.atan2(1 - eventProgress, 1 - durationProgress) * 2 / math.pi
            eventPriority = max(0, min(1, eventPriority))
            #print(eventProgress, durationProgress, eventPriority)

            #https://lukeboyle.com/blog-posts/2016/04/google-calendar-api---color-id
            length = len(priorityColorIds)
            newColor = priorityColorIds[math.floor(eventPriority * (length - 1))]
            event['colorId'] = newColor

            try:
                #https://developers.google.com/calendar/v3/reference/events/update
                service.events().update(calendarId='primary', eventId=event['id'], sendNotifications=False, body=event).execute()
            except Exception as e:
                print('Error Updating Calendar Data: ', e)
                time.sleep(.5)
                continue
