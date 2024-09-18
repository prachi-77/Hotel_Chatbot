**Setup**
Use Python 3.8 and refer https://learning.rasa.com/installation/ for installation.

Refer **Installation Manual** attached in this git repo for detailed steps.

**Run below commands in separate windows after setup**

$ rasa shell ( to open Rasa bot for conversations)

$ rasa run actions (to run Rasa custom actions)

# Hotel Booking Chatbot
This project presents the development and implementation of a hotel booking chatbot leveraging the open-source framework Rasa NLU https://learning.rasa.com/conversational-ai-with-rasa/introduction-to-rasa/. The chatbot is directed towards users who are seeking assistance and information related to hotel bookings. This includes individuals looking to book hotel stays, inquire about existing reservations, or gather 
general information about the hotel's services and facilities. 

**Scope of Chatbot**

We are going to build a chatbot named GrandGuideBot for booking hotel stays. This bot will assist users in booking, cancelling reservations, and providing basic information about our hotel. Let's outline what our chatbot will do:
1. The GrandGuideBot should be able to understand greetings and reply with a greeting.
2. The bot should be able to understand if the user is asking about booking a room, requesting cancellation or seeking general hotel information like location, check-in and check-out times, restaurant hours, nearby tourist spots, and available facilities.
3. The bot should be able to prompt users for details such as their name, contact number for authorization, the number of guests, check-in/check-out dates, and the preferred payment method.
4. After obtaining user details, the bot must offer choices for room types—single, deluxe, or suite. Additionally, it should allow users to decide if they want to include breakfast in their package.
5. The bot should let users cancel their bookings by asking for their name and booking ID.
6. It should also furnish users with general information about the hotel, such as the availability of various cuisine restaurants, spas, swimming pools, gaming zones, and their operating hours, upon user inquiry.
7. Upon successful booking or cancellation, it should prompt user by asking if there is anything else it can help with.

**Intents**

Some of the possible intents are -
1. **Greeting Intent:** User initiates the conversation with a greeting.
2. **BookRoom Intent:** User expresses an intent to book a hotel room.
3. **ProvideDetails Intent:** User shares personal details like name, contact number, and booking 
preferences.
4. **SelectRoomType Intent:** User indicates a preference for a specific type of room (single, deluxe, or 
suite).
5. **SelectBreakfastOption Intent:** User decides whether to include breakfast in the booking.
6. **CancelBooking Intent:** User expresses an intent to cancel an existing booking.
7. **SelectPaymentMethod Intent:** User decides the mode of payment.
8. **GeneralInformation Intent:** User seeks general details about the hotel, such as location, check-in/out 
times, and available facilities.
9. **EnquireAboutServices Intent:** User asks about various services offered by the hotel, such as 
restaurants, spas, swimming pools, and gaming zones.
10. **ThankYou Intent:** User expresses gratitude or thanks after receiving assistance.
11. **BotIdentity Intent:** User asks the bot if it is a human or a bot, or inquires about the bot's identity


**Bot Screenhots**

**Case 1: USER INTENTS TO BOOK A ROOM**

<img width="599" alt="image" src="https://github.com/user-attachments/assets/a3ba8fc1-44de-4b1f-8cd0-d3c8c85608cd">

**Case 2: USER INTENTS TO CANCEL THEIR EXISTING BOOKING**

<img width="564" alt="image" src="https://github.com/user-attachments/assets/0c626e74-ec20-4df0-a2bb-8e5ecdd2191b">

**Case 3: USER SEEKS HOTEL INFORMATION**

<img width="536" alt="image" src="https://github.com/user-attachments/assets/4395e4fd-c941-4fbf-a0c2-70d39f0e480d">


