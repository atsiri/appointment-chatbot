# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"
from __future__ import print_function

from rasa_sdk.events import AllSlotsReset
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
#from database.db_connector import DataInsert, DataSelect
import datetime
from datetime import datetime, timedelta
import dateparser
import os.path
import pandas as pd
import csv

class AddEventToCalendarCSV(Action):

    def name(self) -> Text:
        return "action_add_event"
        
    @staticmethod
    def required_slots(tracker):
        return [
            'user_name',
            'date',
            'session'
            ]

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot('user_name')
        date = tracker.get_slot('date')
        session = tracker.get_slot('session')
        print(session)
        print(type(session))
        datetxt = dateparser.parse(date, settings={'RETURN_AS_TIMEZONE_AWARE': True}).strftime('%Y-%m-%d')
        starttime = dateparser.parse(date, settings={'RETURN_AS_TIMEZONE_AWARE': True}).strftime('%Y-%m-%d %H:%M')
        interval_type = 'minutes'
        interval_num = int(session)
        endtime = (dateparser.parse(starttime) + timedelta(**{interval_type: interval_num})).strftime('%Y-%m-%d %H:%M')

        #insert appintment to db, but currently error due to endpoint issue
        #DataInsert(user_name, datetxt, starttime, endtime, datetime.now())
        #insert to csv db
        op = open("database/db_appointments.csv", "r") 
        df_app = pd.DataFrame(csv.DictReader(op)).reset_index(drop=True).iloc[: , 1:]
        df_new_row = pd.DataFrame([[user_name, datetxt, starttime, endtime, datetime.now()]], columns=df_app.columns)
        df_exist = df_app[df_app.start_time.isin(df_new_row.start_time)]
        #check if the slot time is available
        if len(df_exist) > 0:
            message = "Sorry, the schedule is not available. Would you like to pick another time?"
            dispatcher.utter_message(text=message)
            return []

        #add new appointment if slot time available
        new_appointment = {'Name':user_name, 'day_date':datetxt, 'start_time':starttime,
            'end_time':endtime, 'updated_at':datetime.now()}
        df_app.loc[len(df_app)] = new_appointment
        df_app.to_csv("database/db_appointments.csv")

        #action success message
        stime = dateparser.parse(date, settings={'RETURN_AS_TIMEZONE_AWARE': True}).strftime('%H:%M')
        etime = (dateparser.parse(starttime) + timedelta(**{interval_type: interval_num})).strftime('%H:%M')
        text=f"Dear {user_name}, your appointment is set at {datetxt}, {stime} - {etime}. See you soon!"
        dispatcher.utter_message(text)

        return [AllSlotsReset()]

class GetEventFromCalendarCSV(Action):

    def name(self) -> Text:
        return "action_get_event"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        #currently only accept name
        user_name = tracker.get_slot('user_name')

        #DataInsert(user_name, datetxt, starttime, endtime, datetime.now())
        #open csv
        op = open("database/db_appointments.csv", "r") 
        df_app = pd.DataFrame(csv.DictReader(op)).reset_index(drop=True).iloc[: , 1:]
        
        #check if name exist in appointment
        df_exist = df_app[df_app.Name == user_name]
        if len(df_exist) < 1:
            message = "Sorry, we could not find your appointment. \nWould you like to set a new appointment?"
            dispatcher.utter_message(text=message)
            return []

        #retrieve info
        datetxt = (df_exist['day_date'].values[0])#.strftime('%Y-%m-%d')
        stime = (df_exist['start_time'].values[0])#.strftime('%H:%M')
        etime = (df_exist['end_time'].values[0])#.strftime('%H:%M')
        text=f"Dear {user_name}, your appointment is set at {datetxt}, {stime} - {etime}. See you soon!"
        dispatcher.utter_message(text)

        return [AllSlotsReset()]

# class AddEventToCalendarDB(Action):

#     def name(self) -> Text:
#         return "action_add_event"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         user_name = tracker.get_slot('user_name')
#         date = tracker.get_slot('date')
#         session = tracker.get_slot('session')
#         print(session)
#         print(type(session))
#         datetxt = dateparser.parse(date, settings={'RETURN_AS_TIMEZONE_AWARE': True}).strftime('%Y-%m-%d')
#         starttime = dateparser.parse(date, settings={'RETURN_AS_TIMEZONE_AWARE': True}).strftime('%Y-%m-%d %H:%M')
#         interval_type = 'minutes'
#         interval_num = int(session)
#         endtime = (dateparser.parse(starttime) + timedelta(**{interval_type: interval_num})).strftime('%Y-%m-%d %H:%M')

#         #data_exist = DataSelect

#         DataInsert(user_name, datetxt, starttime, endtime, datetime.now())
#         stime = starttime.strftime('%H:%M')
#         etime = endtime.strftime('%H:%M')
#         text=f"Dear {user_name}, your appointment is set at {datetxt}, {stime} - {etime}. See you soon!"
#         dispatcher.utter_message()

#         return [AllSlotsReset()]

# class getEvent(Action):

#     def name(self) -> Text:
#         return "action_get_event"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         event_name = get_event()

#         print(event_name)
#         #confirmed_event = tracker.get_slot(Any)
#         dispatcher.utter_message(text="got events {name}".format(name= event_name))
#         return []



   
 