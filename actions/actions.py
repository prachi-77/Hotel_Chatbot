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

def get_no_of_rooms(slot_val):
    ppl_digit = [int(s) for s in slot_val.split() if s.isdigit()][0]
    no_of_rooms = 0
    text = 'rooms'
    if ppl_digit%2 == 0:
        no_of_rooms = (int(ppl_digit/2))
            
    else:
        no_of_rooms = int(ppl_digit/2)
        no_of_rooms +=1
    text = ['room' if no_of_rooms ==1 else 'rooms']
    return [no_of_rooms,text[0]]

def extract_duration(value):
    # Regular expression pattern to match numerical value and unit
    if isinstance(value,int):
        return value
    elif value.isdigit() :
        return int(value)
    else:
        pattern = r'(\d+)\s*(day|week|night|nights|weeks)'
        match = re.match(pattern, value, re.IGNORECASE)
        if match:
            # Extract numerical value and unit
            duration = int(match.group(1))
            unit = match.group(2).lower()
            
            # Convert to standard unit (e.g., days)
            if unit in ['week', 'weeks']:
                duration *= 7
            elif unit in ['night', 'nights']:
                pass  
            return duration
        else:
            return None  # Return None if no match found
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
        # dispatcher.utter_message(text=f"Hey {value} !")
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
            error_message = "\033[91mError: You can only book room from today to a maximum of 3 months from now. Kindly check your date.\033[0m"
            dispatcher.utter_message(
                text=error_message
            )
            
            return {"check_in_date": None}
        
        return {"check_in_date": slot_value}
    
    def validate_stay_duration(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Text]:

        stay_days = extract_duration(slot_value)
        if stay_days is None:
            dispatcher.utter_message("Please enter a valid number for stay duration.")
            return {"stay_duration": None}
        check_in_date = datetime.strptime(tracker.get_slot("check_in_date"), '%d/%m/%Y')
        check_out_date = check_in_date + timedelta(days=stay_days)
        dispatcher.utter_message(f"Your check-out date will be : {check_out_date} ")
        return {"stay_duration": stay_days}
       
            

    def validate_num_people(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        ppl_digit = [int(s) for s in slot_value.split() if s.isdigit()][0]
        
        if ppl_digit == 0:
            error_message = "\033[91mError: Minimum 1 person is required for booking.\033[0m"
            dispatcher.utter_message(
                text=error_message
            )
            return {"num_people": None}
        room_info = get_no_of_rooms(slot_value)
        no_of_rooms = room_info[0]
        text = room_info[1]
       
        dispatcher.utter_message(f"As maximum of 2 people are allowed per room. "
                                 f"You will have to book {no_of_rooms} {text}. ")
        return {"num_people": slot_value}
    
    # def validate_breakfast_option(
    #     self,
    #     value: Any,
    #     dispatcher: CollectingDispatcher,
    #     tracker: Tracker,
    #     domain: DomainDict,
    # ) -> Dict[Text, Any]:
    #     if value.lower() not in ["yes", "no"]:
    #         dispatcher.utter_message("Please select either 'Yes' or 'No'.")
    #         return {"breakfast_option": None}
    #     return {"breakfast_option": value}

    def validate_payment_mode(
        self,
        slot_value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: DomainDict,
    ) -> Dict[Text, Any]:
        print("payment",slot_value)
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
        room_info = get_no_of_rooms(num_people)
        no_of_rooms = room_info[0]
        text = room_info[1]
        stay_days = extract_duration(slot_values.get("stay_duration"))
        check_in_date = datetime.strptime(tracker.get_slot("check_in_date"), "%d/%m/%Y")
        check_out_date = check_in_date + timedelta(days=stay_days)
        dispatcher.utter_message(f"Congratulations {name}!\n"
                                 f"You have booked {no_of_rooms} {room_type} {text} for {num_people}.\n"
                                 f"Check-in Date :  {check_in_date} , Check-out Date : {check_out_date}\n"
                                 f"Mode of Payment :  {payment_mode}.")
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
                "stay_duration"
                "num_people",
                "room_type",
                # "breakfast_option",
                "payment_mode"]
    def slot_mappings(self) -> Dict[Text, Any]:
        return {
            "name": self.from_entity(entity="name", intent="user_utters_for_name"),
            "phone": self.from_entity(entity="phone", intent="ProvideDetails"),
            "check_in_date": self.from_entity(entity="check_in_date", intent="ProvideDetails"),
            "stay_duration": self.from_entity(entity="stay_duration", intent="ProvideDetails"),
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

