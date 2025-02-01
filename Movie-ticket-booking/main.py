import json
from Bots.pvr_booking_bot import book_pvr_ticket

# Read input and config files
with open('Input/input.json') as f:
    input_data = json.load(f)

with open('Config/navigation.json') as f:
    navigation_config = json.load(f)

# Run the bot function
book_pvr_ticket(input_data, navigation_config)
