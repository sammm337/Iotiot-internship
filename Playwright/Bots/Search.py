import json
import time
import logging
from playwright.sync_api import sync_playwright

# Configure logging
logging.basicConfig(filename="Logs/botactivity.log", level=logging.INFO, format="%(asctime)s - %(message)s")

def search_tickets():
    logging.info("Starting ticket search...")
    
    # Load user inputs from the JSON file
    with open("Input/user_inputs.json", "r") as file:
        tasks = json.load(file)

    task = tasks[0]  # Processing the first task
    
    # Extract details from the content field
    task_content = task["content"]
    inputs = {
        "origin": task_content.split("Origin: ")[1].split(",")[0].strip(),
        "destination": task_content.split("Destination: ")[1].split(",")[0].strip(),
        "departure_date": task_content.split("Departure Date: ")[1].split(",")[0].strip(),
        "return_date": task_content.split("Return Date: ")[1].split(",")[0].strip(),
        "travel_class": task_content.split("Travel Class: ")[1].split(",")[0].strip(),
        "passenger_count": int(task_content.split("Passenger Count: ")[1].strip())
    }
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        page = browser.new_page()
        
        # Navigate to the website
        page.goto("https://www.makemytrip.com/")  # Replace with the actual website URL
        time.sleep(3)  # Allow the page to load fully
        
        # Handle login popup
        try:
            close_button = page.wait_for_selector('//*[@id="SW"]/div[1]/div[2]/div[2]/div/section/span', timeout=5000)
            close_button.click()
            logging.info("Login popup closed.")
        except:
            logging.info("No login popup found.")

        # Select Origin
        page.click('//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/label/p/span')
        page.fill('//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div/input', inputs["origin"])
        time.sleep(2)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        # Select Destination
        page.click('//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/label/span')
        page.fill('//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div/input', inputs["destination"])
        time.sleep(2)
        page.keyboard.press("ArrowDown")
        page.keyboard.press("Enter")

        # Handle Departure Date Selection
        page.click('//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[3]/label/span')
        time.sleep(3)  # Wait for the calendar to load

        departure_date = inputs['departure_date']  # Example: 'Feb 24 2025'
          # Format: 'Mon Feb 24 2025'

# Locate the date element based on aria-label
        date_element = page.locator(f'//div[@class="DayPicker-Day" and @aria-label="{departure_date}"]')

# Wait for the date element to be visible and clickable
        date_element.wait_for(state='visible', timeout=10000)  # Wait for 10 seconds for visibility
        date_element.click()
        logging.info(f"Selected departure date: {departure_date}")
       
# Handle Return Date Selection
        page.click('//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[4]/div[2]/label/span')
        time.sleep(5)  # Wait for the calendar to load

# Find the return date element based on the date text (e.g., '20' for the 20th)
        return_date = inputs['return_date']  # Example: 'Feb 20 2025'
         # Format: 'Mon Feb 20 2025'
        date_element = page.locator(f'//div[@class="DayPicker-Day" and @aria-label="{return_date}"]')

# Wait for the date element to be visible and clickable
        date_element.wait_for(state='visible', timeout=10000)  # Wait for 10 seconds for visibility
        date_element.click()
        logging.info(f"Selected return date: {return_date}")


        # Click the search button
        page.click('//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/p/a')
        time.sleep(10)  # Allow results to load

        # Prepare output data
        output_data = {
            "task_id": task["task_id"],
            "status": "success",
            "message": "Ticket search completed successfully.",
            "details": inputs
        }

        # Write to output.json on successful completion
        with open("output.json", "w") as output_file:
            json.dump(output_data, output_file, indent=4)
        
        logging.info(f"Output written to output.json for task {task['task_id']}.")

        browser.close()

if __name__ == "__main__":
    search_tickets()
