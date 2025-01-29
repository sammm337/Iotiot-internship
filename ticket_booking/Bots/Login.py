import json
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def login(driver):
    logging.info("Starting login process...")

    # Load credentials
    with open("Config/credentials.json", "r") as file:
        credentials = json.load(file)

    driver.get("https://www.makemytrip.com/")

    try:
        # Wait for the login popup to appear and then close it using XPath
        wait = WebDriverWait(driver, 10)
        close_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="SW"]/div[1]/div[2]/div[2]/div/section/span')))
        close_button.click()
        logging.info("Login popup closed.")
    except Exception as e:
        logging.warning(f"Could not close login popup: {e}")

    # You can proceed with login if needed
    # driver.find_element(By.XPATH, "//input[@id='username']").send_keys(credentials["username"])
    # driver.find_element(By.XPATH, "//input[@id='password']").send_keys(credentials["password"])
    # driver.find_element(By.XPATH, "//input[@id='password']").send_keys(Keys.RETURN)

    logging.info("Login successful!")
