# This files contains your custom actions which can be used to run custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import requests
from geopy.geocoders import Nominatim


class ActionLocation(Action):

    def name(self) -> Text:
        return "action_get_location"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        loc_type = tracker.get_slot("locationType")
        pincode = tracker.get_slot("pincode")

        msg = "Sorry! the servers are currently busy"

        URL = f"https://api.postalpincode.in/pincode/{pincode}"
        try: 
            r = requests.get(url=URL)
            data = r.json()
            if data[0]['Message'] == 'No records found':
                msg = "Sorry, that's an invalid PIN!"
            else:
                if loc_type == 'state':
                    msg = f"The state is {data[0]['PostOffice'][0]['State']}"
                elif loc_type == 'city' or loc_type:
                    msg = f"The city is {data[0]['PostOffice'][0]['Region']}"
                elif loc_type == 'district'or loc_type:
                    msg = f"The district is {data[0]['PostOffice'][0]['District']}"
        except: # if the api is unavailable
            geolocator = Nominatim(user_agent="geoapiExercises")
            data = geolocator.geocode(pincode)[0].split(",")
            if loc_type == 'state':
                    msg = f"The state is {data[-3]}"
            elif loc_type == 'city' :
                msg = f"The city is {data[2]}"
            elif loc_type == 'district':
                msg = f"The district is {data[3]}"


        dispatcher.utter_message(text=msg)

        return []
