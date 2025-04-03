import time
from playwright.sync_api import sync_playwright
import json

def write_log(log_entry):
    """Helper function to write log entries to a .log file"""
    with open('Logs/botactivity.log', 'a') as log_file:
        timestamp = time.strftime("%Y-%m-%dT%H:%M:%S")
        log_file.write(f"{timestamp} - {log_entry}\n")

def book_pvr_ticket(input_data, navigation_config):
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set headless=True for silent execution
        page = browser.new_page()
        
        # Start Logging Activity
        write_log("Started browser session")

        # Navigate to PVR website
        page.goto(navigation_config["base_url"])
        write_log("Navigated to PVR Cinemas")

        # Select City
        page.fill(navigation_config["city_input_xpath"], input_data["city"])
        page.wait_for_timeout(2000)  # Wait for suggestions
        page.wait_for_timeout(5000)  # Allow transition
        write_log(f"Selected city: {input_data['city']}")

        # Select Movie (Deva)
        page.click(navigation_config["movie_dropdown_xpath"])
        page.wait_for_timeout(2000)
        page.click(navigation_config["movie_option_xpath"])
        write_log("Selected movie: DEVA")

        # Select First Available Date
        page.wait_for_timeout(2000)
        page.click(navigation_config["date_option_xpath"])  # First option
        write_log("Selected first available date")

        # Select First Available Cinema
        page.wait_for_timeout(2000)
        page.click(navigation_config["cinema_option_xpath"])  # First option
        write_log("Selected first available cinema")

        # Select First Available Showtime (Ignoring Disabled)
        page.wait_for_timeout(2000)
        available_time = page.locator(navigation_config["first_available_time_xpath"]).first
        available_time.click()
        write_log("Selected first available showtime")

        # Click Book
        page.wait_for_timeout(2000)
        page.click(navigation_config["book_button_xpath"])
        write_log("Clicked Book button")

        # Accept Terms & Conditions
        page.wait_for_timeout(3000)
        page.click(navigation_config["accept_button_xpath"])
        write_log("Accepted terms and conditions")

        # Select Farthest Seat from Screen
        page.wait_for_timeout(3000)
        farthest_row = page.locator(navigation_config["farthest_row_xpath"])

        # Find available seats in the farthest row (seat should have 'seat-current-pvr' but NOT 'seat-disable')
        available_seats = farthest_row.locator(".seat-current-pvr:not(.seat-disable)").all()

        # Select the first valid seat
        if available_seats:
            available_seats[0].click()
            write_log("Selected the farthest available seat")

        # Click Proceed
        page.wait_for_timeout(2000)
        page.click(navigation_config["proceed_button_xpath"])
        write_log("Clicked Proceed button")

        # Log completion status
        output_data = {
            "task_id": input_data["task_id"],
            "status": "Completed",
            "completion_time": time.strftime("%Y-%m-%dT%H:%M:%S")
        }

        # Write output status to output.json
        with open('Output/output.json', 'w') as f:
            json.dump(output_data, f, indent=4)

        # Close Browser
        page.wait_for_timeout(5000)
        browser.close()
        write_log("Closed the browser session")



