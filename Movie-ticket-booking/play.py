from playwright.sync_api import sync_playwright

def book_pvr_ticket():
    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False)  # Set headless=True for silent execution
        page = browser.new_page()
        
        # Navigate to PVR website
        page.goto("https://www.pvrcinemas.com/")
        
        # Select City
        page.fill("//input[@placeholder='Search for city']", "Pune")
        page.wait_for_timeout(2000)  # Wait for suggestions
        # page.click("(//li[contains(@class, 'p-dropdown-item')])[1]")
        page.wait_for_timeout(5000)  # Allow transition

        # Select Movie (Deva)
        page.click('//*[@id="movie"]/span')
        page.wait_for_timeout(2000)
        page.click("//li[contains(@class, 'p-dropdown-item')]/span[text()='DEVA']")

        # Select First Available Date
        page.wait_for_timeout(2000)
        page.click("(//li[contains(@class, 'p-dropdown-item')])[1]")  # First option

        # Select First Available Cinema
        page.wait_for_timeout(2000)
        page.click("(//li[contains(@class, 'p-dropdown-item')])[1]")  # First option

        # Select First Available Showtime (Ignoring Disabled)
        page.wait_for_timeout(2000)
        available_time = page.locator("//li[contains(@class, 'p-dropdown-item') and not(contains(@class, 'disabled'))]").first
        available_time.click()

        # Click Book
        page.wait_for_timeout(2000)
        page.click('//*[@id="root"]/div[4]/div[2]/div/div/div/div/div/form/div/div[7]/button')

        # Accept Terms & Conditions
        page.wait_for_timeout(3000)
        page.click("//button[text()='Accept']")

        # Select Farthest Seat from Screen
        page.wait_for_timeout(3000)
        page.wait_for_timeout(3000)  # Wait for seats to load
        farthest_row = page.locator('//*[@id="root"]/section/div/div/div[1]/div[3]/div/div[3]/div/div/tr[9]')

# Find available seats in the farthest row (seat should have 'seat-current-pvr' but NOT 'seat-disable')
        available_seats = farthest_row.locator(".seat-current-pvr:not(.seat-disable)").all()

# Select the first valid seat
        if available_seats:
            available_seats[0].click()
        
        # Click Proceed
        page.wait_for_timeout(2000)
        page.click("//button[text()='Proceed']")

        # Close Browser
        page.wait_for_timeout(5000)
        browser.close()

# Run the function
book_pvr_ticket()
