# LinkedIn Automation Bot

## Description/Overview
The LinkedIn Automation Bot is a Python-based automation tool designed to streamline LinkedIn interactions using Selenium. It automates tasks like post scheduling, helping users maintain an active LinkedIn presence without manual effort. The bot operates securely with user-defined schedules and configurations to ensure controlled and efficient automation.

## Features
* **Automated Post Scheduling** – Users can define posts and schedule them in input.json, ensuring timely content updates.
* **Task-Based Execution** – Each task is assigned a Task ID for structured logging and tracking.
* **Secure Authentication** – Login credentials are stored securely in config.json to ensure account safety.
* **Activity Logging** – Every action is logged in log.txt, making it easy to review and debug past operations.

## How to use the bot:
1. Add your correct credentials in the Config/credentials file
2. Install the dependencies: `pip3 install selenium`
3. Run the file on terminal using the command: `python3 Run/main.py`
4. If verification code is asked, provide the code manually
5. You will have to change the xpaths of the elements according to your computer. Go to the specific element and click on inspect, then click on the copy xpath option. Xpaths will change across different pcs and browsers so make sure you add the correct xpath by inspecting the element.
6. You will have to add the xpaths for "start a post" and "click post button" steps.

## Contact
In case of bugs contact me at: samruddhis307@gmail.com

## Credits & Acknowledgments
This project was undertaken as part of my internship, where I developed a LinkedIn posts system using selenium to automate the process of posting on linkedin. I would like to express my sincere gratitude to IoTIoT for their invaluable guidance and support throughout the project.

A special thanks to Nikhil Bhaskaran, Founder of IoTIoT, for his mentorship and insightful direction, which greatly contributed to the successful completion of this work. I also extend my appreciation to Sneha Bhapkar for her valuable support and assistance during the process.