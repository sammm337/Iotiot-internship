File Structure:
FlightBookingBot/
│
├── Bots/
│   └── flight_booking_bot.py      # Contains Playwright bot logic for booking flights
│
├── Config/
│   ├── credentials.json           # Stores login credentials (if needed)
│   └── navigation.json            # Contains URLs and XPaths for navigation
│
├── Input/
│   └── input.json                 # Contains task ID, flight details, passenger info, etc.
│
├── Logs/
│   └── botactivity.log            # Logs of bot activities (steps performed)
│
├── Output/
│   └── output.json                # Contains task ID, completion status, and timestamp
│
└── main.py                        # Main script to run the flight booking bot
