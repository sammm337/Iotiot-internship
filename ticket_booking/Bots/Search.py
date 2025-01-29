from selenium.webdriver.common.by import By
import json
import logging
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def search_tickets(driver):
    logging.info("Starting ticket search...")
    
    # Load user inputs from the JSON file
    # with open("Input/user_inputs.json", "r") as file:
    #     inputs = json.load(file)
    
    # # Wait for and interact with the "From" input field
    # WebDriverWait(driver, 100).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="originInput-input"]'))
    # )
    # driver.find_element(By.XPATH, '//*[@id="originInput-input"]').send_keys(inputs["origin"])

    # # Wait for and interact with the "To" input field
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.ID, "destinationInput-input"))
    # )
    # driver.find_element(By.ID, "destinationInput-input").send_keys(inputs["destination"])





    # # Wait for and click the "Departure Date" button to open the date picker dialog
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="outboundDatePickerInput"]/div/button/p[2]'))
    # )
    # driver.find_element(By.XPATH, '//*[@id="outboundDatePickerInput"]/div/button/p[2]').click()

    # # Wait for the date picker dialog to appear, then select the departure date
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="mobile"]/div/div/div[2]/div[6]/div/div/div/div/div/div[1]/div/div/div/div[5]/div[3]/div/div/button/span'))  # Replace with the actual XPath of the date picker dialog
    # )
    # driver.find_element(By.XPATH, '//*[@id="mobile"]/div/div/div[2]/div[6]/div/div/div/div/div/div[1]/div/div/div/div[5]/div[3]/div/div/button/span').click()  # Replace with the actual XPath of the selected departure date



    # # Wait for and click the "Return Date" button to open the return date picker dialog
    # WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.XPATH, '//*[@id="inboundDatePickerInput"]/div/button/p[1]'))
    # )
    # driver.find_element(By.XPATH, '//*[@id="inboundDatePickerInput"]/div/button/p[1]').click()

    # # Wait for the return date picker dialog to appear, then select the return date
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="mobile"]/div/div/div[2]/div[6]/div/div/div/div/div/div[2]/div/div/div/div[1]/div[7]/div/div/button/span'))  # Replace with the actual XPath of the return date picker dialog
    # )
    # driver.find_element(By.XPATH, '//*[@id="mobile"]/div/div/div[2]/div[6]/div/div/div/div/div/div[2]/div/div/div/div[1]/div[7]/div/div/button/span').click()  # Replace with the actual XPath of the selected return date

    # # Wait for and click the "Search" button to submit the search form
    # WebDriverWait(driver, 10).until(
    #     EC.presence_of_element_located((By.XPATH, '//*[@id="app-root"]/div[1]/div/main/div[1]/div/div[3]/div/div/button'))
    # )
    # driver.find_element(By.XPATH, '//*[@id="app-root"]/div[1]/div/main/div[1]/div/div[3]/div/div/button').click()
    time.sleep(1000) # Waits up to 1000 seconds if needed before throwing an error

    logging.info("Search completed!")
