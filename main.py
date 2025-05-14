from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

import time

# Correct data types
PHONE = "+14375595074"
LOCATION = "Ajax, Ontario, Canada"

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)
wait = WebDriverWait(driver, 15)

def abort_application():
    try:
        # Click Close Button
        close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
        close_button.click()
        time.sleep(2)

        # Click Discard Button if it appears
        discard_buttons = driver.find_elements(By.XPATH, "//button/span[text()='Discard']")
        if discard_buttons:
            discard_buttons[0].click()
            time.sleep(2)
    except Exception as e:
        print(f"Error while aborting application: {e}")

# LinkedIn credentials
linkedin_email = "aimykehinde@gmail.com"
linkedin_password = "1@!myK@y2"

# Step 1: Log in to LinkedIn
driver.get("https://www.linkedin.com/login")
wait.until(EC.presence_of_element_located((By.ID, "username")))
driver.find_element(By.ID, "username").send_keys(linkedin_email)
driver.find_element(By.ID, "password").send_keys(linkedin_password)
driver.find_element(By.XPATH, "//button[@type='submit' and contains(.,'Sign in')]").click()

# Pause to solve CAPTCHA manually
input("🔐 Press Enter after solving the CAPTCHA...")

# Step 2: Go to Jobs page
wait.until(EC.presence_of_element_located((By.ID, "global-nav-search")))
driver.get("https://www.linkedin.com/jobs/")

# Step 3: Search for job title and location
wait.until(EC.presence_of_element_located((By.XPATH, "//input[contains(@aria-label, 'Search by title, skill, or company')]")))

job_search_box = driver.find_element(By.XPATH, "//input[contains(@aria-label, 'Search by title, skill, or company')]")
job_search_box.clear()
job_search_box.send_keys("Contract Analyst")

location_search_box = driver.find_element(By.XPATH, "//input[contains(@aria-label, 'City, state, or zip code')]")
location_search_box.clear()
location_search_box.send_keys("Greater Toronto Area, Canada")
location_search_box.send_keys(Keys.ENTER)

# Wait for job listings to load
time.sleep(5)
all_listings = driver.find_elements(By.CSS_SELECTOR, ".job-card-container--clickable")

# Step 4: Apply to each listing
for listing in all_listings:
    print("📄 Opening job listing...")
    listing.click()
    time.sleep(3)

    try:
        apply_button = driver.find_element(By.CSS_SELECTOR, ".jobs-s-apply button")
        if apply_button.text.strip() != "Easy Apply":
            print("⏭️ Not an Easy Apply job, skipping.")
            continue
        apply_button.click()
        time.sleep(3)

        # Insert Phone Number
        try:
            phone = driver.find_element(By.CSS_SELECTOR, "input[id*=phoneNumber]")
            if phone.get_attribute("value").strip() == "":
                phone.clear()
                phone.send_keys(PHONE)
        except NoSuchElementException:
            print("⚠️ Phone number input not found.")

        # Insert Location
        try:
            location = driver.find_element(By.CSS_SELECTOR, "input[id*=location]")
            if location.get_attribute("value").strip() == "":
                location.clear()
                location.send_keys(LOCATION)
                location.send_keys(Keys.ENTER)
        except NoSuchElementException:
            print("⚠️ Location input not found.")

        # Handle "Next" or "Submit"
        while True:
            try:
                submit_button = driver.find_element(By.XPATH, "//button[contains(@aria-label, 'Submit application')]")
                print("✅ Submitting application...")
                submit_button.click()
                break
            except NoSuchElementException:
                try:
                    next_button = driver.find_element(By.XPATH, "//button/span[text()='Next']")
                    print("➡️ Clicking next...")
                    next_button.click()
                    time.sleep(2)
                except NoSuchElementException:
                    print("❌ Complex multi-step application detected.")
                    abort_application()
                    break

        time.sleep(2)

        # Close the modal
        try:
            close_button = driver.find_element(By.CLASS_NAME, "artdeco-modal__dismiss")
            close_button.click()
        except NoSuchElementException:
            print("ℹ️ Close button not found.")

    except NoSuchElementException:
        print("❌ Apply button not found, skipping.")
        continue

# Final step - keep browser open for review
input("✅ Done! Press Enter to close the browser...")
driver.quit()
