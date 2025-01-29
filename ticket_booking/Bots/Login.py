from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import json
import logging

def login(driver):
    logging.info("Starting login process...")
    with open("Config/credentials.json", "r") as file:
        credentials = json.load(file)
    
    driver.get("https://www.skyscanner.co.in/")
    # driver.find_element(By.ID, "username").send_keys(credentials["username"])
    # driver.find_element(By.ID, "password").send_keys(credentials["password"])
    # driver.find_element(By.ID, "password").send_keys(Keys.RETURN)
    logging.info("Login successful!")
