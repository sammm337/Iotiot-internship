import os
import time
import logging
import json
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Logging setup
logging.basicConfig(
    filename=os.path.join("Logs", "botactivity.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Paths
INPUT_FILE = os.path.join("Input", "input.json")
CREDENTIALS_FILE = os.path.join("Config", "credentials.csv")
OUTPUT_FILE = os.path.join("Output", "output.json")

def load_credentials():
    """Loads LinkedIn login credentials from credentials.csv"""
    try:
        df = pd.read_csv(CREDENTIALS_FILE, encoding='utf-8')
        return df.Username[0], df.Password[0]
    except Exception as e:
        logging.error(f"Failed to load credentials: {e}")
        return None, None

def load_input_data():
    """Loads input data from input.json"""
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        logging.error(f"Failed to load input data: {e}")
        return []

def save_output_data(output_data):
    """Saves output data to output.json"""
    try:
        os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=4)
    except Exception as e:
        logging.error(f"Failed to save output data: {e}")

def linkedin_post_bot():
    """Logs into LinkedIn and posts multiple updates"""
    
    # Load credentials
    username, password = load_credentials()
    if not username or not password:
        return

    # Load input posts
    posts = load_input_data()
    if not posts:
        logging.error("No posts found in input.json")
        return
    
    # Initialize WebDriver
    driver = webdriver.Chrome()
    driver.maximize_window()

    try:
        logging.info("Navigating to LinkedIn login page.")
        driver.get("https://www.linkedin.com/login")

        logging.info("Logging in.")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.ID, "username"))
        ).send_keys(username)

        driver.find_element(By.ID, "password").send_keys(password + Keys.RETURN)

        # Wait for login to complete
        time.sleep(5)

        output_data = []

        for post in posts:
            task_id = post["task_id"]
            post_content = post["content"]

            try:
                logging.info(f"Starting post for Task ID: {task_id}")

                # Refresh the page before each post
                driver.refresh()
                time.sleep(5)  # Allow page to reload

                # Click "Start a post"
                post_button = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//strong[text()='Start a post']]"))
                )
                post_button.click()
                logging.info("Clicked 'Start a post' button.")

                # Enter post content
                post_box = WebDriverWait(driver, 20).until(
                    EC.presence_of_element_located((By.XPATH, "//div[@role='textbox']"))
                )
                post_box.send_keys(post_content)
                logging.info("Entered post content.")

                # Click "Post" button
                WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//button[.//span[text()='Post']]"))
                ).click()
                logging.info(f"Post published successfully for Task ID: {task_id}")

                # Wait for post to be processed
                time.sleep(5)

                # Append status to output
                output_data.append({"task_id": task_id, "status": "completed"})

            except Exception as e:
                logging.error(f"Error posting Task ID {task_id}: {e}")
                output_data.append({"task_id": task_id, "status": "failed"})

        # Save results
        save_output_data(output_data)

    except Exception as e:
        logging.error(f"Error in LinkedIn bot: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    linkedin_post_bot()