import logging
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys  # Import Keys for Enter key
import json
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_tickets(driver):
    logging.info("Starting ticket search...")
    
    # Load user inputs from the JSON file
    with open("Input/user_inputs.json", "r") as file:
        tasks = json.load(file)

    # Assuming we are processing the first task
    task = tasks[0]
    
    # Extract details from the content field of the task
    task_content = task["content"]
    
    # Parse the content string to get individual details
    inputs = {
        "origin": task_content.split("Origin: ")[1].split(",")[0].strip(),
        "destination": task_content.split("Destination: ")[1].split(",")[0].strip(),
        "departure_date": task_content.split("Departure Date: ")[1].split(",")[0].strip(),
        "return_date": task_content.split("Return Date: ")[1].split(",")[0].strip(),
        "travel_class": task_content.split("Travel Class: ")[1].split(",")[0].strip(),
        "passenger_count": int(task_content.split("Passenger Count: ")[1].strip())
    }

    # Wait for the 'From' field to load and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/label/p/span'))
    ).click()

    # Enter the origin city
    origin_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[1]/div[1]/div/div/div/input'))
    )
    origin_input.send_keys(inputs["origin"])
    time.sleep(2)  # Wait for suggestions to appear

    # Select the first suggestion
    origin_input.send_keys(Keys.ARROW_DOWN)
    origin_input.send_keys(Keys.RETURN)
    
    # Wait for the 'To' field to load and click it
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/label/span'))
    ).click()

    # Enter the destination city
    destination_input = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/div[1]/div[2]/div[1]/div/div/div/input'))
    )
    destination_input.send_keys(inputs["destination"])
    time.sleep(2)  # Wait for suggestions to appear

    # Select the first suggestion
    destination_input.send_keys(Keys.ARROW_DOWN)
    destination_input.send_keys(Keys.RETURN)
    time.sleep(10)
    # Click the search button
    WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, '//*[@id="top-banner"]/div[2]/div/div/div/div/div[2]/p/a'))
    ).click()

    time.sleep(15)  # Give time for results to load
    
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

