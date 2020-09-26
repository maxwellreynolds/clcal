#!/usr/bin/env python
from __future__ import print_function
import sys
import argparse
import datetime
import pickle
import os.path
import json
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from termcolor import colored, cprint
import argparse
from os.path import join



num_events = 10
max_days = None


parser = argparse.ArgumentParser()
parser.add_argument("--events", "-e", help="set to maximum number of events")
parser.add_argument("--days", "-d", help="set to maximum number of days forward to show (today is 0)")
args=parser.parse_args()

if args.events:
    num_events = args.events

if args.days:
    max_days = args.days


dir=os.path.join(os.path.dirname(__file__))

#colors
colorDict={
    '5':'yellow',
    '1':'magenta',
    '2':'green',
    '-1':'blue'
}

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


"""Shows basic usage of the Google Calendar API.
Prints the start and name of the next 10 events on the user's calendar.
"""
creds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists(os.path.join(dir,'token.pickle')):
    with open(os.path.join(dir,'token.pickle'), 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            os.path.join(dir,'credentials.json'), SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open(os.path.join(dir,'token.pickle'), 'wb') as token:
        pickle.dump(creds, token)

service = build('calendar', 'v3', credentials=creds)

# Call the Calendar API
now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC tim

if max_days is not None:
    max_date = (datetime.datetime.utcnow()+datetime.timedelta(int(max_days)))
    max_datetime = datetime.datetime(max_date.year,max_date.month,max_date.day, 23, 59, 59, 464551)
    max_tstamp = float(max_datetime.strftime("%s"))
    max_utc = datetime.datetime.utcfromtimestamp(max_tstamp).isoformat()+'Z'
    print(max_utc)
    # exit()
    events_result = service.events().list(calendarId='primary', timeMin=now, timeMax = max_utc,
                                    maxResults=num_events, singleEvents=True,
                                    orderBy='startTime').execute()


else:
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                    maxResults=num_events, singleEvents=True,
                                    orderBy='startTime').execute()

events = events_result.get('items', [])

if not events:
    print('No upcoming events found.')
ev_date = None
for event in events:
    start = event['start'].get('dateTime', event['start'].get('date'))
    end = event['end'].get('dateTime', event['start'].get('date'))
    description = '\n' + event['description'].replace('<p>',' ').replace('</p>',' ').replace('&nbsp;',' ').replace('<br>',' ').replace('\n',' ') if 'description' in event and 'zoom' in event['description'] else ''
    if start[:10]!= ev_date:
        ev_date = start[:10]
        cprint('\n'+ev_date,attrs=['bold'])
    color=colorDict[event['colorId']] if 'colorId' in event and event['colorId'] in colorDict else 'blue'
    if color:
        cprint(start[11:-6]+' - '+end[11:-6]+ ' ' + event['summary'] + ' ', color, end='')
        print(description)
    else:
        print(start[11:-6],'-',end[11:-6], event['summary'], description)
