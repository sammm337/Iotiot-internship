import os
import time
import logging
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logging.basicConfig(
    filename=os.path.join("Logs", "botactivity.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def linkedin_post_bot():
    # Load credentials
    try:
        df = pd.read_csv(os.path.join("Config", "credentials.csv"), encoding='utf-8')
        myUsername = df.Username[0]
        myPassword = df.Password[0]
        myPost = df.Post[0]
    except Exception as e:
        logging.error(f"Failed to load credentials: {e}")
        return

    # Initialize WebDriver
    driver = webdriver.Chrome()  # Ensure chromedriver is in PATH
    driver.maximize_window()

    try:
        logging.info("Navigating to LinkedIn login page.")
        driver.get("https://www.linkedin.com/login")

        logging.info("Logging in.")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(myUsername)

        driver.find_element(By.ID, "password").send_keys(myPassword + Keys.RETURN)

        # Wait for login to complete
        time.sleep(5)

        logging.info("Clicking 'Start a post'.")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Start a post')]"))
        ).click()

        logging.info("Entering post content.")
        post_box = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
        )
        post_box.send_keys(myPost)

        logging.info("Publishing post.")
        WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@aria-label, 'Post')]"))
        ).click()

        logging.info("Post published successfully!")

    except Exception as e:
        logging.error(f"Error in LinkedIn bot: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    linkedin_post_bot()
