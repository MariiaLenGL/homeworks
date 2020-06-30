#!/usr/bin/python

"""
   1. Setup Google Calendar APi - https://developers.google.com/calendar/quickstart/python
   2. Create a simple calender event - https://developers.google.com/calendar/create-events
   3. Add 'sergii.tishchenko@globallogic.com' into notification
   4. Analize event structure
   5. Create metaclass that will update google api event respond into class object
   6. Modify created event object description variable
   7. Update calendar event on server side

"""

from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import json


def connection_api():
    """
    Connection to google API
    (Is fully copied from google)
    """
    # If modifying these scopes, delete the file token.pickle.
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('calendar', 'v3', credentials=creds)


def load_event(event_id):
    event = connection_api().events().get(calendarId='primary', eventId=event_id).execute()
    return event


class SomeMetaClass(type):
    def __new__(cls, class_name, bases, clsdict):
        clsdict.update(load_event("u3on342ospb29m0rvpmgvpfvn8"))
        cls_obj = super().__new__(cls, class_name, bases, clsdict)
        return cls_obj

class Event(metaclass=SomeMetaClass):
    def __init__(self, **kwargs):
        for key in kwargs:
            self.__dict__[key] = kwargs[key]
    
    @classmethod
    def serialize(cls, event):
        event_dict_json = json.dumps(event.__dict__)
        json_event = json.loads(event_dict_json)
        return json_event 

    @classmethod
    def create_from_file(cls, file_path: str) -> "Event":
        with open(file_path, encoding="utf8") as f:
            event = cls(**json.load(f))
            event = Event.serialize(event)
            event = connection_api().events().insert(calendarId='primary', body=event).execute()
            print('Event created: %s' % (event.get('htmlLink')))
        return event.get('id')
      
    @classmethod
    def update_event(cls, event_id, update_dict):
        event = connection_api().events().get(calendarId='primary', eventId=event_id).execute()
        for key in update_dict:
            event[key] = update_dict[key]
        updated_event = connection_api().events().update(calendarId='primary', eventId=event['id'], body=event).execute()
        print('Event updated: %s' % (event.get('htmlLink')))
        return updated_event.get('id')


if __name__ == '__main__':
    print("Creating event from sample_event.json...")
    event = Event.create_from_file(os.path.abspath("sample_event.json"))
    
    print("Updating description and attendee...")
    update_dict = {"description": "New description", "attendees": [{"email": "sergii.tishchenko@globallogic.com"}]}
    Event.update_event(event, update_dict)
    
    print("Checking response statuses...")
    event_loaded = load_event(event)

    for i in range(len(Event.attendees)):
        for key in Event.attendees[i]:
            print('{}:{}'.format(key, Event.attendees[i][key]))