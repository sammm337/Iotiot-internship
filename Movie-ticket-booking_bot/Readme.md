# Movie Ticket Booking Bot

## Description
This bot automates the process of booking a movie ticket on the PVR Cinemas website using Playwright. It selects a city, chooses a movie, picks the first available date, cinema, and showtime, then selects the farthest available seat. The bot also accepts terms and conditions, proceeds with the booking, and logs all actions in a .log file. The completion status is saved in output.json.

## Features

* **Automated Movie Ticket Booking**: Selects city, movie, date, cinema, and showtime dynamically.

* **Seat Selection Logic**: Identifies and selects the farthest available seat from the screen.

* **Terms & Conditions Handling**: Automatically accepts terms before proceeding.

* **Error Handling & Logging**: Logs every step in a .log file for tracking and debugging.

* **Dynamic Interaction**: Waits for elements, handles dropdowns, and selects only available showtimes.

## How to use this bot:
1. Install dependencies: `pip3 install playwright`
2. Run the command in the terminal: `python3 play.py`
3. Click on the city
4. The bot will choose the movie, date, cinema and time
5. It will redirect you to a different page and automatically accept the terms and conditions
6. It will select a seat in the last row and click on the proceed button

## Contact
In case of bugs contact me at: samruddhis307@gmail.com

## Credits & Acknowledgments
This project was undertaken as part of my internship, where I developed a movie ticket booking system using playwright. I would like to express my sincere gratitude to IoTIoT for their invaluable guidance and support throughout the project.

A special thanks to Nikhil Bhaskaran, Founder of IoTIoT, for his mentorship and insightful direction, which greatly contributed to the successful completion of this work. I also extend my appreciation to Sneha Bhapkar for her valuable support and assistance during the process.