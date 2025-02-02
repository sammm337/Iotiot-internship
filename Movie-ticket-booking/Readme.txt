Used Playwright
File Structure:
Project/
│
├── Bots/
│   └── pvr_booking_bot.py       # Contains your Playwright bot logic
│
├── Config/
│   ├── credentials.json         # Stores any login credentials (if applicable)
│   └── navigation.json          # Contains URLs and XPaths for navigation
│
├── Input/
│   └── input.json               # Contains task id, movie name, number of seats
│
├── Logs/
│   └── botactivity.json         # Logs of bot activities (such as steps performed)
│
└── Output/
    └── output.json              # Contains task id, completion status, and time
│
└── main.py                      # Main script to run the bot
