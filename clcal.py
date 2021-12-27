#!/usr/bin/env python
from __future__ import print_function
import sys
import argparse
import datetime
import pickle
import os.path
import pdb
import json
from time import strptime
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from termcolor import colored, cprint
import argparse
from os.path import join
from tzlocal import get_localzone
from util import is_short_date_format, is_short_time_format



num_events = 10
max_days = None


parser = argparse.ArgumentParser()
parser.add_argument("--max_events", "-me", help="set to maximum number of events")
parser.add_argument("--max_days", "-md", help="set to maximum number of days forward to show (today is 0)")
parser.add_argument("--create", "-c", help="create an event", action='store_true')
parser.add_argument("--startdate", "-sd", help="start datetime for created event. \nformat as yyyy-mm-dd or mm-dd (defaults to current year)")
parser.add_argument("--starttime", "-st", help="start time. \nformat as hh:mm:ss or hh:mm")
parser.add_argument("--enddate", "-ed", help="end datetime for created event. set to start time if empty")
parser.add_argument("--endtime", "-et", help="end time")
parser.add_argument("--summary", "-s", help="name of event")
parser.add_argument("--description", "-d", help="description of event")


args=parser.parse_args()

# print(args)





if args.max_events:
    num_events = args.max_events

if args.max_days:
    max_days = args.max_days



dir=os.path.join(os.path.dirname(__file__))

#colors
colorDict={
    '5':'yellow',
    '1':'magenta',
    '2':'green',
    '-1':'blue'
}

# If modifying these scopes, delete the file token.pickle.
# SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
SCOPES = ['https://www.googleapis.com/auth/calendar']



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

if not args.create:
    if max_days is not None:
        max_date = (datetime.datetime.utcnow()+datetime.timedelta(int(max_days)))
        max_datetime = datetime.datetime(max_date.year,max_date.month,max_date.day, 23, 59, 59, 464551)
        max_tstamp = float(max_datetime.strftime("%s"))
        max_utc = datetime.datetime.utcfromtimestamp(max_tstamp).isoformat()+'Z'
        # print(max_utc)
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


##Create event
if args.create:
    print('creating event:')
    tz = get_localzone()
    d = datetime.datetime.now(tz) #get utcoffset in current timezone
    utc_offset = d.utcoffset().total_seconds()
    utc_offset=int(utc_offset//3600)
    neg=utc_offset < 0
    abs_utc_offset=abs(utc_offset)
    utc_str=('-' if neg else '+') + str(abs_utc_offset).zfill(2) + ':00'

    assert(args.startdate)
    sd=args.startdate
    if sd.lower()=='today':
        sd=str(datetime.date.today().year)+'-'+str(datetime.date.today().month)+'-'+str(datetime.date.today().day)
    elif sd.lower()=='tomorrow':
        tomorrow=datetime.date.today()+datetime.timedelta(days=1)
        sd=str(tomorrow.year)+'-'+str(tomorrow.month)+'-'+str(tomorrow.day)
    elif(is_short_date_format(sd)):
        sd=str(datetime.date.today().year) + '-' + sd
        # print('fixed sd:',sd)
    assert(args.starttime)
    st=args.starttime
    if is_short_time_format(st): #add 0 seconds if in short time format
        # print('appending :00 to s')
        st=st+':00'

    # print('start date:',sd)
    # print('start time',st)
    start_dt_string=sd+'T'+st
    start_dt_string_with_offset=start_dt_string + utc_str
    # print('input startdtstr:',start_dt_string_with_offset)

    #datetime object for start datetime
    start_datetime=datetime.datetime.strptime(start_dt_string,'%Y-%m-%dT%H:%M:%S')


    # assert(args.enddate)
    # pdb.set_trace()
    #if no end date or time, default to 1 hr after start
    if args.enddate is None and args.endtime is None:
        end_datetime=start_datetime+datetime.timedelta(hours=1)
        ed=end_datetime.strftime('%Y-%m-%d')
        et=end_datetime.strftime('%H:%M:%S')
    elif not args.enddate is None and args.endtime is None:
        raise RuntimeError("add end time if you add end date")
    else:
        et=args.endtime
    if is_short_time_format(et): #add 0 seconds if in short time format
        et=et+':00'
    if args.enddate is None and not args.endtime is None:
        end_datetime=datetime.datetime.strptime(sd+'T'+et,'%Y-%m-%dT%H:%M:%S')
        if end_datetime < start_datetime:
            end_datetime = end_datetime+datetime.timedelta(days=1)
        ed=end_datetime.strftime('%Y-%m-%d')
    if not args.enddate is None and not args.endtime is None:
        ed=args.enddate
        if ed.lower()=='today':
            ed=str(datetime.date.today().year)+'-'+str(datetime.date.today().month)+'-'+str(datetime.date.today().day)
        elif ed.lower()=='tomorrow':
            tomorrow=datetime.date.today()+datetime.timedelta(days=1)
            ed=str(tomorrow.year)+'-'+str(tomorrow.month)+'-'+str(tomorrow.day)
        elif(is_short_date_format(ed)):
            ed=str(datetime.date.today().year) + '-' + ed
            # print('fixed ed:',ed)
    
    # print('end date:',ed)
    # print('end time',et)
    end_dt_string=ed+'T'+et
    end_dt_string_with_offset=end_dt_string+utc_str

    summary=args.summary
    # print('summary:',summary)

    new_event={
        'summary':summary,
        'start':{'dateTime':start_dt_string_with_offset},
        'end':{'dateTime':end_dt_string_with_offset},
        'description':args.description
    }

    event = service.events().insert(calendarId='primary', body=new_event).execute()  
    print(event['summary'],event['status'], '\nfor',event['start']['dateTime'],event['start']['timeZone'],'\nto',
    event['end']['dateTime'])

# test_event={
#   'summary': 'Google I/O 2015',
#   'location': '800 Howard St., San Francisco, CA 94103',
#   'description': 'A chance to hear more about Google\'s developer products.',
#   'start': {
#     'dateTime': '2021-12-28T09:00:00-05:00',
#     'timeZone': 'America/New_York',
#   },
#   'end': {
#     'dateTime': '2021-12-28T17:00:00-05:00',
#     'timeZone': 'America/New_York',
#   },
#   'attendees': [
#     {'email': 'lpage@example.com'},
#     {'email': 'sbrin@example.com'},
#   ],
#   'reminders': {
#     'useDefault': False,
#     'overrides': [
#       {'method': 'email', 'minutes': 24 * 60},
#       {'method': 'popup', 'minutes': 10},
#     ],
#   },
# }