# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet

class ActionConfirmBooking(Action):

    def name(self) -> Text:
        return "utter_confirm_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        user_name = tracker.get_slot("name")
        room_type = tracker.get_slot("room_type")
        price = "100 USD"
        dispatcher.utter_message("Congratulations {} ! Your {} room booking is confimed. Total bill - {}".format(user_name,room_type,price))

        return [SlotSet("price",price)]
