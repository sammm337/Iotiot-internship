import logging
from selenium import webdriver
from Bots.Login import login
from Bots.Search import search_tickets
from Bots.Checkout import checkout
import json

# Configure logging
logging.basicConfig(filename="Logs/botactivity.log", level=logging.INFO, format="%(asctime)s - %(message)s")

# Load config
with open("Config/navigation_config.json", "r") as file:
    config = json.load(file)

# Initialize WebDriver
driver = webdriver.Chrome()  # Ensure chromedriver is installed

try:
    logging.info("Script started...")
    driver.get(config["url"])
    
    # Run bots
    login(driver)
    search_tickets(driver)
    # checkout(driver)
    
    logging.info("Automation completed successfully!")
finally:
    driver.quit()
