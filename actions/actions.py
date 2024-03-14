# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


from typing import Any, Text, Dict, List
from datetime import datetime, timedelta
from rasa_sdk import Action, Tracker, FormValidationAction,forms
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet,EventType,ActiveLoop
from rasa_sdk.types import DomainDict
import re
ALLOWED_ROOM_TYPES = ["deluxe", "single", "suite"]

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

class ValidateSimpeUserForm(FormValidationAction):
    def name(self) -> Text:
        return "validate_simple_user_form"

    def validate_name(
        self,
        value: Text,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        # Validate that the name is not empty
        if not value.strip():
            dispatcher.utter_message("Please provide a non-empty name.")
            # Set the slot to None to request the user to provide the name again
            return {"name": None}

        # Validate that the name doesn't contain special characters
        if not re.match("^[a-zA-Z0-9_]*$", value):
            dispatcher.utter_message("Name should not contain special characters.")
            return {"name": None}

        # Validation passed, set the slot value
        dispatcher.utter_message(text=f"OK! You want a booking under {value} name.")
        return {"name": value}

    def validate_room_type(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate `room_type` value."""

        if slot_value not in ALLOWED_ROOM_TYPES:
            error_message = "\033[91mError: I don't recognize that room type.\033[0m"
            dispatcher.utter_message(
                text=error_message
            )
           
            return {"room_type": None}
        dispatcher.utter_message(text=f"OK! You want to book a {slot_value} room.")
        return {"room_type": slot_value}

    def validate_phone(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate phone_number value."""
        # Add your validation logic for phone_number here
       
        if len(slot_value)!=10:
            error_message = "\033[91mError: Kindly enter a valid phone number.\033[0m"
            dispatcher.utter_message(
                text=error_message
            )
            return {"phone": None}
        return {"phone": slot_value}

    def validate_check_in_date(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate check_in_date value."""
        given_date_string = slot_value

        # Parse the given date string
        given_date = datetime.strptime(given_date_string, '%d/%m/%Y').date()

        # Get today's date
        today = datetime.now().date()
      
        # Calculate the date 3 months from now
        three_months_from_now = today + timedelta(days=3 * 30)

        # Check if the given date falls within the range
        if not(today <= given_date <= three_months_from_now):
            error_message = "\033[91mError: You can only book room from today to a maximum of 3 months now. Kindly check your date.\033[0m"
            dispatcher.utter_message(
                text=error_message
            )
            
            return {"check_in_date": None}
        
        return {"check_in_date": slot_value}

    def validate_payment_mode(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        
        if slot_value not in ['credit card','debit card','cash','Gpay']:
            error_message = "\033[91mError: Invalid payment mode.\033[0m"
            dispatcher.utter_message(
                text=error_message
            )
            
            return {"payment_mode": None}
        slot_values = tracker.current_slot_values()
        name = slot_values.get("name")
        room_type = slot_values.get("room_type")
        num_people = slot_values.get("num_people")
        payment_mode = slot_values.get("payment_mode")
        dispatcher.utter_message(f"Congratulations {name}! "
                                 f"You have booked a {room_type} room for {num_people}. "
                                 f"Your payment will be made through {payment_mode}.")
        return []
    def validate(self, dispatcher, tracker, domain):
        if tracker.latest_message['intent']['name'] == "SelectPaymentMethod":
            dispatcher.utter_message(
                text=f"exiting custom form. byebye.thanks,love ya"
            )
            return None  # Empty list signals form completion
        else:
            return super().validate(dispatcher, tracker, domain)
    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("name")
        # Perform any necessary actions with the validated user_name
        dispatcher.utter_message(f"Deactivating form, Thank you, {user_name}!")
        return None
    
class SimpleUserForm(FormValidationAction):
    def name(self) -> Text:
        return "simple_user_form"

    def required_slots(tracker: Tracker) -> List[Text]:
        return ["name", 
                "phone", 
                "check_in_date",
                "num_people",
                "room_type",
                # "breakfast_option",
                "payment_mode"]
    def slot_mappings(self) -> Dict[Text, Any]:
        return {
            "name": self.from_entity(entity="name", intent="user_utters_for_name"),
            "phone": self.from_entity(entity="phone", intent="ProvideDetails"),
            "check_in_date": self.from_entity(entity="check_in_date", intent="ProvideDetails"),
            # "check_out_date": self.from_entity(entity="check_out_date", intent="ProvideDetails"),
            "num_people": self.from_entity(entity="number_of_people", intent="ProvideDetails"),
            "room_type": self.from_entity(entity="room_type", intent="SelectRoomType"),
            # "breakfast_option": self.from_entity(entity="breakfast_option", intent="SelectBreakfastOption"),
            "payment_mode": self.from_entity(entity="payment_mode", intent="SelectPaymentMethod"),
        }

    def request_next_slot(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        """Request the next slot and utter template if needed."""
        for slot in self.required_slots(tracker):
            if tracker.slots.get(slot) is None:
                dispatcher.utter_message(template=f"utter_ask_{slot}")
                return [SlotSet("requested_slot", slot)]
        return None

   

    

    
    
  
    def validate_payment_mode(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        """Validate check_in_date value."""
        if slot_value not in ['credit card','debot card']:
            dispatcher.utter_message(
                text=f"Invalid pay,ent mode."
            )
            return {"payment_mode": None}
        dispatcher.utter_message(text=f"OK! You want to book a {slot_value} cash.")
        return [SlotSet("requested_slot", None)]
        # return[SlotSet(SlotSet("name", None),
        #                SlotSet("phone", None),
        #                SlotSet("check_in_date", None),
        #                SlotSet("num_people", None),
        #                SlotSet("room_type", None),
        #                SlotSet("payment_mode", None))]

    def validate(self, dispatcher, tracker, domain):
        if tracker.latest_message['intent']['name'] == "SelectPaymentMethod":
            dispatcher.utter_message(
                text=f"exiting custom form. byebye."
            )
            return None  # Empty list signals form completion
        else:
            return super().validate(dispatcher, tracker, domain)

    def submit(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("name")
        # Perform any necessary actions with the validated user_name
        dispatcher.utter_message(f"Deactivating form, Thank you, {user_name}!")
        return None  # Return None to signal form completion
       
        # Deactivate the form
        # return [Form(None), SlotSet("requested_slot", None)]


class ActionUtterRoomType(Action):
    def name(self) -> Text:
        return "utter_room_type"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        room_type = tracker.get_slot("room_type")
        dispatcher.utter_message(f"We have {room_type} rooms available.")
        return []

class ActionConfirmBooking(Action):
    def name(self) -> Text:
        return "utter_confirm_booking"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        user_name = tracker.get_slot("user_name")
        room_type = tracker.get_slot("room_type")
        breakfast_option = tracker.get_slot("breakfast_option")
        payment_mode = tracker.get_slot("payment_mode")
        # Add other slots as needed

        dispatcher.utter_message(f"Congratulations {user_name}! "
                                 f"You have booked a {room_type} room with {breakfast_option} breakfast. "
                                 f"Your payment will be made through {payment_mode}.")
        return []

