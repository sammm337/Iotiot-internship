import time
import json
import webbrowser
import pyautogui
import os
from pathlib import Path
from pynput.keyboard import Controller, Key
import sys
from p_logging_utils import setup_logger

keyboard = Controller()

# Setup logger
logger = setup_logger('take_screenshots')

def open_linkedin_profile_and_screenshot(json_file):
    """Opens LinkedIn profile and takes a full-page screenshot."""
    try:
        logger.info("Starting LinkedIn screenshot process...")
        
        # Load LinkedIn URL from output.json
        if not os.path.exists(json_file):
            logger.error(f"JSON file not found: {json_file}")
            return False

        with open(json_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        linkedin_url = data.get("LinkedIn", None)
        
        if not linkedin_url:
            logger.error("No LinkedIn profile found!")
            return False

        # Create Input directory if it doesn't exist
        screenshots_dir = Path(__file__).resolve().parent.parent / "Input"
        screenshots_dir.mkdir(parents=True, exist_ok=True)

        # Open LinkedIn profile in default web browser
        logger.info(f"Opening LinkedIn Profile: {linkedin_url}")
        webbrowser.open(linkedin_url)
        
        # Wait for browser to load - adjustable based on internet speed
        logger.info("⏳ Waiting for page to load...")
        time.sleep(10)  # Increased wait time for slower connections

        # Scroll down to load full profile
        for cnt in range(1, 11):
            screenshot_file = screenshots_dir / f"linkedin_screenshot{cnt}.png"
            
            try:
                screenshot = pyautogui.screenshot()
                screenshot.save(str(screenshot_file))
                logger.info(f"Screenshot {cnt}/10 saved as: {screenshot_file}")
            except Exception as e:
                logger.error(f"Error taking screenshot {cnt}: {e}")
                continue

            # Gentle scrolling
            keyboard.press(Key.page_down)
            keyboard.release(Key.page_down)
            time.sleep(2.5)  # Increased delay between scrolls

        return True

    except Exception as e:
        logger.error(f"Error during screenshot process: {e}", exc_info=True)
        return False

def main():
    # Update paths using Path for cross-platform compatibility
    BASE_DIR = Path(__file__).resolve().parent.parent
    output_json = str(BASE_DIR / "Output" / "p_output.json")

    if not open_linkedin_profile_and_screenshot(output_json):
        sys.exit(1)

if __name__ == "__main__":
    main()
